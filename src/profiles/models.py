from django.db import models
from django.conf import settings
# Create your models here.


from django.contrib.auth.models import AbstractUser
User = settings.AUTH_USER_MODEL

class User(AbstractUser):
	print("****")
	print("Hi i'm in the user model")
	def get_profile_url(self):
		return f"/habit/{self}"



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile", null=True)
	birthdate = models.DateField(null=True, blank=True)
	account_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['account_creation_date'] #the order of these is the order that comments will be sorted by

	def __str__(self):
		return self.user.username


#basically a static version of the User get_profile_url
	@staticmethod
	def get_profile_url(username):
		return f"/habit/{username}"



#Need to do blank = something null = something for this eventually to avoid errors
class ProfileFollow(models.Model):
	follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profiles_followed")
	followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.follower.__str__() + " followed " + self.followee.__str__()

	class Meta:
		ordering = ['timestamp'] #the order of these is the order that comments will be sorted by

	@staticmethod
	def get_profile_total_followers(profile):
		return len(ProfileFollow.objects.filter(followee=profile))

	@staticmethod
	def get_profile_total_followees(profile):
		return len(ProfileFollow.objects.filter(follower=profile))
			