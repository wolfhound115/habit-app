from django import template
from habits.models import CommentLike, PostLike, PostComment
from profiles.models import Profile




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

@register.simple_tag
def is_profile_followed_by_user(profile_user, user):
	print("profile_user is: " + profile_user.__str__() +", user is: " + user.__str__())
	print("****")
	print("****")
	if user.is_authenticated:
		return profile_user.user_profile.followers.filter(follower=user.user_profile).exists()
	else:
		return False

@register.simple_tag
def is_user_followed_by_profile_user(profile_user, user):
	if user.is_authenticated:
		return user.user_profile.followers.filter(follower=profile_user.user_profile).exists()
	else:
		return False
	

@register.simple_tag
def get_user_profile_url(user):
	return user.get_profile_url

@register.simple_tag
def get_likes_formatted(likes):
	if not likes:
		return ""
	elif likes == 1:
		return "1 like"
	else:
		return "" + str(likes) + " likes"

@register.simple_tag
def get_profile_url(username):
	return Profile.get_profile_url(username)