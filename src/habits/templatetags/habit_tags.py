from django import template
from habits.models import CommentLike, PostLike, PostComment



register = template.Library()

@register.simple_tag
def is_comment_liked_by_user(comment, user):
	return CommentLike.objects.filter(user=user, comment=comment).exists()

@register.simple_tag
def is_post_liked_by_user(post, user):
	return PostLike.objects.filter(user=user, post=post).exists()

@register.simple_tag
def is_this_owned_by_user(content_owner, user):
	if user.is_authenticated:
		return content_owner == user
	else:
		return False