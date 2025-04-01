# categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:pk>/', views.category_detail, name='category_detail'),
    path('new/', views.create_category, name='create_category'),
    path('<int:pk>/edit/', views.update_category, name='update_category'),
    path('<int:pk>/delete/', views.delete_category, name='delete_category'),
]
