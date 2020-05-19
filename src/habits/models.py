from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


# HabitPost is each individual picture/desc upload
# Title could be some default habitName Day __
# Description is also optional

User = settings.AUTH_USER_MODEL

class HabitPost(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) #n not sure what user data to store
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=2200)
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-publish_date', '-timestamp'] #the order of these is the order that posts will be sorted by
