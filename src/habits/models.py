from django.db import models
from django.conf import settings
from django.utils import timezone


from django.contrib.auth.models import AbstractUser

from recurrence.fields import RecurrenceField

from django.db.models.signals import post_save
from django.dispatch import receiver
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
	recurrences = RecurrenceField(null=True)
	start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)


# TODO Limit queryset for habit posts in the habit post creation form to only valid tracks for today's date for this user
# Do this when implementing CRUD for posts
# https://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform

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








class HabitEvent(HabitModel):
	track = models.ForeignKey(HabitTrack, on_delete=models.CASCADE, null=False)

	date_expected = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False) #make null=false later
	post = models.OneToOneField(HabitPost, on_delete=models.SET_NULL, null=True, blank=True)


def generate_habit_events(track, dates):

	#HabitEvent.objects.bulk_create([HabitEvent(track=track, date=d) for d in dates])

	for d in dates:
		HabitEvent.objects.create(track=track, date_expected=d)
	
	#TODO
	#streak counter
	#	get queryset of all events for this track before today inclusive, sort, and iterate through list counting how many before instance.post not none
	#	we know from snapchat that people like streaks!

# may need to disconnect/reconnect if this is causing recursive save calls
# weak – Django stores signal handlers as weak references by default. 
# Thus, if your receiver is a local function, it may be garbage collected. To prevent this, pass weak=False when you call the signal’s connect() method.

@receiver(post_save, sender=HabitTrack, dispatch_uid="generate_empty_habit_events")
def post_save_habit_tracks(sender, instance, created, *args, **kwargs):
	print("*******")
	print("post save habit tracks reciever")
	if created:
		datetimes = instance.recurrences.occurrences(

			# might also want to add dtend for efficiency later

			dtstart=instance.start_date
		)

		dates = [dt.date() for dt in datetimes] #this removes the time from the datetime

		generate_habit_events(instance, dates)


# TODO Do something if today isn't a valid day to post, or limit the option to post from before this step
@receiver(post_save, sender=HabitPost, dispatch_uid="connect_habit_event_foreign_key_to_this_post")
def post_save_habit_posts(sender, instance, created, *args, **kwargs):

	if created:
		event = HabitEvent.objects.filter(user=instance.user).filter(track=instance.track).filter(date_expected=instance.timestamp.date()).first()
		event.post = instance
		event.save() #this will save only the event column instead of the entire row
		print(event)

