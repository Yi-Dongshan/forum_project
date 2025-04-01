# notifications/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/mark-read/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('api/notifications/unread-count/', views.unread_notification_count, name='notification_count'),
]