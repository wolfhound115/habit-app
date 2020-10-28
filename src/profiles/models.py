from django.db import models
from django.conf import settings
# Create your models here.


from django.contrib.auth.models import AbstractUser


from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL


import os
import random


#this is to avoid image name overlaps and organize user file uploads
def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(50))
    return 'image/userphotos/{userid}/{randomstring}{ext}'.format(userid= instance.user.id, randomstring= randomstr, ext= file_extension)



class User(AbstractUser):
	print("****")
	print("Hi i'm in the user model")
	def get_profile_url(self):
		return f"/habit/{self}"



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile", null=True)
	birthdate = models.DateField(null=True, blank=True)
	profile_bio = models.CharField(max_length=2200, null=True, blank=True)
	profile_image = models.ImageField(upload_to=photo_path, blank=False, null=True)
	account_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['account_creation_date'] #the order of these is the order that comments will be sorted by

	def __str__(self):
		return self.user.username


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
			

#this is so in the registration form email is checked for uniqueness too because its stored in the default user model
User=get_user_model()
User._meta.get_field('email')._unique = True