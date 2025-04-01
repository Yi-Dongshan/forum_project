from django.shortcuts import render
from django.db.models import Count, Q  # 添加 Q 导入
from django.contrib.auth.models import User
from posts.models import Post
from categories.models import Category
from django.utils import timezone
from datetime import timedelta

def home(request):
    # 获取最新的5篇帖子
    latest_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
    
    # 获取最近30天内帖子数最多的5个分类
    thirty_days_ago = timezone.now() - timedelta(days=30)
    popular_categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__created_at__gte=thirty_days_ago))  # 使用 Q 对象
    ).order_by('-post_count')[:5]
    
    # 获取最近30天内发帖最多的5个用户
    active_users = User.objects.annotate(
        post_count=Count('posts', filter=Q(posts__created_at__gte=thirty_days_ago))  # 使用 Q 对象
    ).order_by('-post_count')[:5]
    
    return render(request, 'home.html', {
        'latest_posts': latest_posts,
        'popular_categories': popular_categories,
        'active_users': active_users,
    })