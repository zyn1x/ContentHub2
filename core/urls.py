"""URL patterns for ContentHub2 core app."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('hashtag/<str:name>/', views.hashtag_feed, name='hashtag_feed'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
]
