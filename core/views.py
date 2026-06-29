"""Views for ContentHub2 core app."""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Like, Comment, Hashtag
from .forms import PostForm, CommentForm, CustomUserCreationForm


# ─── Feed ────────────────────────────────────────────────────────────────────

def feed(request):
    """Main feed showing all posts, paginated."""
    posts_qs = Post.objects.select_related('author').prefetch_related('hashtags', 'likes')
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=page_obj.object_list)
            .values_list('post_id', flat=True)
        )

    return render(request, 'core/feed.html', {
        'page_obj': page_obj,
        'liked_ids': liked_ids,
        'comment_form': CommentForm(),
    })


# ─── Post Detail ─────────────────────────────────────────────────────────────

def post_detail(request, pk):
    """Detail view for a single post with comments."""
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('hashtags'), pk=pk)
    comments = post.comments.select_related('author').order_by('created_at')
    user_liked = (
        request.user.is_authenticated
        and Like.objects.filter(post=post, user=request.user).exists()
    )
    comment_form = CommentForm()
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'user_liked': user_liked,
        'comment_form': comment_form,
    })


# ─── Post Create ─────────────────────────────────────────────────────────────

@login_required
def post_create(request):
    """Create a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form, 'action': 'Create'})


# ─── Post Edit ────────────────────────────────────────────────────────────────

@login_required
def post_edit(request, pk):
    """Edit an existing post (owner only)."""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to edit this post.')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


# ─── Post Delete ─────────────────────────────────────────────────────────────

@login_required
def post_delete(request, pk):
    """Delete a post (owner only)."""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to delete this post.')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('feed')
    return render(request, 'core/post_confirm_delete.html', {'post': post})


# ─── Like Toggle ─────────────────────────────────────────────────────────────

@login_required
@require_POST
def like_toggle(request, pk):
    """Toggle like/unlike on a post. Returns JSON for AJAX."""
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.like_count})


# ─── Comment Create ───────────────────────────────────────────────────────────

@login_required
@require_POST
def comment_create(request, pk):
    """Add a comment to a post."""
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Comment added!')
    else:
        messages.error(request, 'Could not add comment. Please check your input.')
    return redirect('post_detail', pk=pk)


# ─── Comment Delete ──────────────────────────────────────────────────────────

@login_required
def comment_delete(request, pk):
    """Delete a comment (owner only)."""
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden('You are not allowed to delete this comment.')
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('post_detail', pk=post_pk)


# ─── Hashtag Feed ─────────────────────────────────────────────────────────────

def hashtag_feed(request, name):
    """Feed filtered by hashtag."""
    hashtag = get_object_or_404(Hashtag, name=name.lower())
    posts_qs = hashtag.posts.select_related('author').prefetch_related('hashtags', 'likes')
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=page_obj.object_list)
            .values_list('post_id', flat=True)
        )

    return render(request, 'core/hashtag_feed.html', {
        'hashtag': hashtag,
        'page_obj': page_obj,
        'liked_ids': liked_ids,
    })


# ─── Search ──────────────────────────────────────────────────────────────────

def search(request):
    """Full-text search across post text and hashtag names."""
    query = request.GET.get('q', '').strip()
    posts_qs = Post.objects.none()

    if query:
        posts_qs = Post.objects.filter(
            Q(text__icontains=query) | Q(hashtags__name__icontains=query.lstrip('#'))
        ).distinct().select_related('author').prefetch_related('hashtags', 'likes')

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_ids = set()
    if request.user.is_authenticated and page_obj.object_list:
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=page_obj.object_list)
            .values_list('post_id', flat=True)
        )

    return render(request, 'core/search_results.html', {
        'query': query,
        'page_obj': page_obj,
        'liked_ids': liked_ids,
    })


# ─── Register ─────────────────────────────────────────────────────────────────

def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to ContentHub, {user.username}!')
            return redirect('feed')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/auth/register.html', {'form': form})
