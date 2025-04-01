# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404  # 添加 get_object_or_404
from django.contrib import messages
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号 {username} 创建成功！现在可以登录了。')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'user_posts': user_posts
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '您的个人资料已更新！')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')  # 或者重定向到 'posts:post_list'


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    return render(request, 'accounts/user_profile.html', {
        'profile_user': user,  # 使用profile_user避免与request.user混淆
        'user_posts': user_posts,
    })