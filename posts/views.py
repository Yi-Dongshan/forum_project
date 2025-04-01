# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from categories.models import Category
from notifications.models import Notification


def post_list(request):
    posts = Post.objects.all()
    
    # 分类过滤
    category_id = request.GET.get('category')
    if category_id:
        try:
            category_id = int(category_id)
            posts = posts.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass  # 如果category_id不是有效的整数，则忽略分类过滤
    
    # 获取搜索参数
    search_query = request.GET.get('search', '').strip()  # 使用空字符串作为默认值，并去除首尾空格
    
    current_category_name = None

    if category_id:
        posts = posts.filter(category_id=category_id)
        # 获取当前分类的名称
        try:
            current_category_name = Category.objects.get(id=category_id).name
        except Category.DoesNotExist:
            pass

    if search_query:
        posts = posts.filter(title__icontains=search_query)

    # 排序
    sort_by = request.GET.get('sort', 'latest')  # 默认改为 'latest'
    if sort_by == 'popular':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    else:  # 'latest'
        posts = posts.order_by('-created_at')

    # 分页
    paginator = Paginator(posts, 10)  # 每页10篇帖子
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_id,
        'current_category_name': current_category_name,
        'search_query': search_query,  # 这里传递处理后的搜索词
        'sort_by': sort_by
    }

    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent=None)

    # 增加浏览量
    post.views += 1
    post.save()

    # 检查用户是否已点赞
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, post=post).exists()

    # 评论表单
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            # 创建通知（如果评论者不是帖子作者）
            if new_comment.author != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    post=post,
                    comment=new_comment,
                    notification_type='comment'
                )

            messages.success(request, '评论发表成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '帖子发布成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        initial_category = request.GET.get('category')
        form = PostForm(initial={'category': initial_category} if initial_category else None)

    return render(request, 'posts/post_form.html', {'form': form, 'title': '发布新帖子'})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 验证当前用户是作者或管理员
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限编辑此帖子")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '帖子已更新！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form, 'title': '编辑帖子'})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 验证当前用户是作者或管理员
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限删除此帖子")

    if request.method == 'POST':
        post.delete()
        messages.success(request, '帖子已删除！')
        return redirect('post_list')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # 创建通知
            if comment.author != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    post=post,
                    comment=comment,
                    notification_type='comment'
                )

            messages.success(request, '评论已添加！')
            return redirect('post_detail', pk=post.pk)

    return redirect('post_detail', pk=post.pk)


@login_required
def reply_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    parent_comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()

            # 创建通知
            Notification.objects.create(
                recipient=parent_comment.author,
                sender=request.user,
                post=post,
                comment=reply,
                notification_type='reply'
            )

            messages.success(request, '回复已添加！')

    return redirect('post_detail', pk=post.pk)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # 创建通知
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                post=post,
                notification_type='like'
            )
    else:
        # 如果已经点过赞，则取消点赞
        like.delete()

    return JsonResponse({
        'likes_count': post.likes_count(),
        'liked': created
    })
