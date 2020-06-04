from django.db import models
from django.conf import settings
from django.utils import timezone


from django.contrib.auth.models import AbstractUser
# Create your models here.


# HabitPost is each individual picture/desc upload
# Title could be some default habitName Day __
# Description is also optional

User = settings.AUTH_USER_MODEL


# Don't need both publish_date and timestamp right
class HabitModel(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) #n not sure what user data to store






#Similar to a facebook album could allow comments on the overall track aswell as individual posts
class HabitTrack(HabitModel):
	track_name = models.CharField(max_length=100)
	description = models.CharField(max_length=2200)
	cover_image = models.ImageField(upload_to='image/', blank=True, null=True)


	#TODO
	#track start date
	#track frequency
	#streak counter
	#
class HabitEvent(HabitModel):
	pass

class HabitPost(HabitModel):
	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=2200)
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	track = models.ForeignKey(HabitTrack, null=True, on_delete=models.SET_NULL)
	#habittrack should be based on foreign key just like user
		#not sure what happens if two users have the same habit name??
	class Meta:
		ordering = ['-publish_date', '-timestamp'] #the order of these is the order that posts will be sorted by
