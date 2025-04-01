# categories/admin.py
from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
