from django.contrib import admin
from reviewapp.models import Products, Reviews


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description', 'image']
    list_display_links = ['id', 'name', 'category', 'description', 'image']
    list_filter = ['name', 'category']
    search_fields = ['id', 'name', 'category']
    fields = ['name', 'category', 'description', 'image']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'description', 'rating', 'is_moderated', 'created_at', 'updated_at']
    list_display_links = ['id', 'author', 'product',]
    search_fields = ['id', 'author', 'product',]
    fields = ['author', 'product', 'description', 'rating', 'is_moderated', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
