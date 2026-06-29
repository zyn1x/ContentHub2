"""Forms for ContentHub2 core app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with email field."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'id': 'id_email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    """Form for creating and editing posts with file validation."""

    class Meta:
        model = Post
        fields = ['text', 'image', 'video']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "What's on your mind? Use #hashtags to categorize your post.",
                'id': 'id_post_text',
                'maxlength': 2000,
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = image.name.rsplit('.', 1)[-1].lower()
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError(
                    f'Unsupported image format. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
                )
            if image.size > MAX_FILE_SIZE_BYTES:
                raise forms.ValidationError('Image file too large. Maximum size is 10 MB.')
        return image

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            ext = video.name.rsplit('.', 1)[-1].lower()
            if ext not in ALLOWED_VIDEO_EXTENSIONS:
                raise forms.ValidationError(
                    f'Unsupported video format. Allowed: {", ".join(ALLOWED_VIDEO_EXTENSIONS)}'
                )
            if video.size > MAX_FILE_SIZE_BYTES:
                raise forms.ValidationError('Video file too large. Maximum size is 10 MB.')
        return video

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text', '').strip()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        if not text and not image and not video:
            raise forms.ValidationError('A post must have text, an image, or a video.')
        return cleaned_data


class CommentForm(forms.ModelForm):
    """Simple comment creation form."""

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'id': 'id_comment_text',
                'maxlength': 1000,
            })
        }
