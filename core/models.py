"""Models for ContentHub2 core app."""

import re
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Hashtag(models.Model):
    """Represents a hashtag used in posts."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'#{self.name}'

    def get_absolute_url(self):
        return reverse('hashtag_feed', kwargs={'name': self.name})


def post_image_upload_path(instance, filename):
    return f'posts/{instance.author.id}/images/{filename}'


def post_video_upload_path(instance, filename):
    return f'posts/{instance.author.id}/videos/{filename}'


class Post(models.Model):
    """A user-created post, optionally containing image or video."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(upload_to=post_image_upload_path, blank=True, null=True)
    video = models.FileField(upload_to=post_video_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at:%Y-%m-%d %H:%M}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Extract and link hashtags from text
        if self.text:
            tags = re.findall(r'#(\w+)', self.text.lower())
            hashtag_objs = []
            for tag in set(tags):
                ht, _ = Hashtag.objects.get_or_create(name=tag)
                hashtag_objs.append(ht)
            self.hashtags.set(hashtag_objs)
        else:
            self.hashtags.clear()


class Like(models.Model):
    """Tracks which user liked which post (unique per user-post pair)."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} liked post #{self.post.pk}'


class Comment(models.Model):
    """A comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on post #{self.post.pk}'
