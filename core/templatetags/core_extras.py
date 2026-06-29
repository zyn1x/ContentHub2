"""Custom template tags and filters for ContentHub2."""

import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='render_hashtags', is_safe=True, needs_autoescape=True)
def render_hashtags(value, autoescape=True):
    """
    Wraps #hashtag tokens in anchor links pointing to the hashtag feed.
    Usage: {{ post.text|render_hashtags }}
    """
    if autoescape:
        escaped = escape(value)
    else:
        escaped = value

    def replace_tag(match):
        tag = match.group(1).lower()
        return f'<a href="/hashtag/{tag}/" class="hashtag-link">#{tag}</a>'

    result = re.sub(r'#(\w+)', replace_tag, escaped)
    return mark_safe(result)
