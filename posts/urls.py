# posts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.update_post, name='update_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_pk>/comment/<int:comment_pk>/reply/', views.reply_comment, name='reply_comment'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
]