from django import template
from habits.models import CommentLike



register = template.Library()

@register.simple_tag
def is_liked_by_user(comment, user):
    return CommentLike.objects.filter(user=user, comment=comment).exists()