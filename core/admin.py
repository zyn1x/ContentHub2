"""Admin configuration for ContentHub2 core app."""

from django.contrib import admin
from .models import Post, Like, Comment, Hashtag


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text_preview', 'created_at', 'like_count', 'comment_count')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')
    filter_horizontal = ('hashtags',)
    date_hierarchy = 'created_at'

    def text_preview(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_preview.short_description = 'Text'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text_preview', 'created_at')
    search_fields = ('text', 'author__username')

    def text_preview(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_preview.short_description = 'Comment'
