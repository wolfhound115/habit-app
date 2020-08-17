from django.db import models
from django.conf import settings
from django.utils import timezone


from django.contrib.auth.models import AbstractUser

from recurrence.fields import RecurrenceField

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from datetime import date



# Create your models here.


# HabitPost is each individual picture/desc upload
# Title could be some default habitName Day __
# Description is also optional

User = settings.AUTH_USER_MODEL


def slug_save(obj):
	""" A function to generate a 5 character slug and see if it has been used and contains naughty words."""
	if not obj.slug: # if there isn't a slug
		obj.slug = get_random_string(11) # create one
		slug_is_wrong = True  
		while slug_is_wrong: # keep checking until we have a valid slug
			slug_is_wrong = False
			other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
			if len(other_objs_with_slug) > 0:
				# if any other objects have current slug
				slug_is_wrong = True
            	#naughty_words = list_of_swear_words_brand_names_etc
            	#if obj.slug in naughty_words:
            	#	slug_is_wrong = True
			if slug_is_wrong:
            	# create another slug and check it again
				obj.slug = get_random_string(11)

# Don't need both publish_date and timestamp right
class HabitModel(models.Model):
	user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL) #n not sure what user data to store
	#def get_profile_url(self):
	#	return f"/habit/{self.user}"


class JustRecurrence(models.Model):
	recurrences = RecurrenceField(null=True)

		
#Similar to a facebook album could allow comments on the overall track aswell as individual posts
class HabitTrack(HabitModel):
	track_name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	description = models.CharField(max_length=2200)
	cover_image = models.ImageField(upload_to='image/', blank=False, null=True)
	recurrences = RecurrenceField(null=True)
	start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)


	def get_num_posts_expected(self):
		return len(self.get_dates())

	def get_all_events(self):
		return HabitEvent.objects.filter(track=self)

	def get_num_posts_made(self):
		return len(self.get_all_events().filter(post__isnull=False))

	def get_post_events_missed(self):
		print(timezone.now().date())
		print(timezone.now().date())
		print(timezone.now())
		print(timezone.now().date())
		print(timezone.now().date())
		all_events = self.get_all_events()
		print("get_post_events_missed")
		print(all_events)
		post_events_missed = all_events.filter(track=self, date_expected__lt=timezone.now().date(), post__isnull=True)
		print(post_events_missed)
		for e in all_events:
			print(e.date_expected)

		return post_events_missed

	def get_num_posts_missed(self):
		return len(self.get_post_events_missed())


#this breaks if you delete a single event because len(dates) and len(all_events) will not be the same then!
	def get_streaks(self):
		dates = self.get_dates()
		all_events = self.get_all_events()
		longest_streak = 0
		streak = 0
		skipped_previous = True
		for d in dates:
			if all_events.get(date_expected=d).post is not None:
				streak += 1
				skipped_previous = False
			elif skipped_previous is False:
				skipped_previous = True
			else:
				longest_streak = max(streak, longest_streak)
				streak = 0
		longest_streak = max(streak, longest_streak)
		return streak, longest_streak

	@staticmethod
	def get_user_habit_stats(user):
		tracks = HabitTrack.objects.filter(user=user)
		total_posts_made = 0
		total_posts_missed = 0
		overall_longest_streak = 0

		for t in tracks:
			total_posts_made += t.get_num_posts_made()
			total_posts_missed += t.get_num_posts_missed()
			#print("getting streaks for habit stats:")
			#print("the track being analyzed is: " + t.__str__())
			#print(t.get_streaks())
			#print("get_streaks worked!!!!")
			#overall_longest_streak = max(overall_longest_streak, t.get_streaks()[1])
		return total_posts_made, total_posts_missed, overall_longest_streak

	def save(self, *args, **kwargs):
		""" Add Slug creating/checking to save method. """
		slug_save(self) # call slug_save, listed below
		super(HabitTrack, self).save(*args, **kwargs)

	def __str__(self):
		return self.track_name

	def get_dates(self):
		print(self.recurrences)
		datetimes = self.recurrences.occurrences(
			# might also want to add dtend for efficiency later
			dtstart=self.start_date
		)
		dates = [dt.date() for dt in datetimes]
		return dates

	class Meta:
		ordering = ['-start_date'] #the order of these is the order that posts will be sorted by

	#this needs to be fixed
	def get_absolute_url(self):
		print("absolute URL track: ")
		print("/habit/{self.user}/tracks/{self.slug}")
		#return f"/habit/{self.user}/tracks/{self.slug}"
		return f"{self.user.get_profile_url()}/tracks/{self.slug}"

	#TODO
	def get_edit_url(self):
		return f"{self.get_absolute_url()}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url()}/delete" #not sure if this works

# TODO Limit queryset for habit posts in the habit post creation form to only valid tracks for today's date for this user
# Do this when implementing CRUD for posts
# https://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform

class HabitPost(HabitModel):

	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=2200)
	image = models.ImageField(upload_to='image/', blank=False, null=True)
	#publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	track = models.ForeignKey(HabitTrack, null=True, on_delete=models.CASCADE)
	#habittrack should be based on foreign key just like user
		#not sure what happens if two users have the same habit name??

	def save(self, *args, **kwargs):
		""" Add Slug creating/checking to save method. """
		slug_save(self) # call slug_save, listed below
		super(HabitPost, self).save(*args, **kwargs)


	class Meta:
		ordering = ['-timestamp'] #the order of these is the order that posts will be sorted by

	#this needs to be fixed
	def get_absolute_url(self):
		print("/habit/{self.user}/posts/{self.slug}")
		return f"{self.user.get_profile_url()}/posts/{self.slug}"

	def get_edit_url(self):
		return f"{self.get_absolute_url()}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url()}/delete" #not sure if this works


class HabitEvent(HabitModel):
	track = models.ForeignKey(HabitTrack, on_delete=models.CASCADE, null=False)
	date_expected = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False) #make null=false later
	post = models.OneToOneField(HabitPost, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.track.__str__() + " " + self.date_expected.strftime("%m/%d/%Y")

	def count_check_ins_expected_today(user):
		events_needing_post_today = HabitEvent.objects.filter(user=user, date_expected=timezone.now().date(), post__isnull=True)
		return len(events_needing_post_today)


class PostComment(HabitModel):
	comment = models.TextField(max_length=300)
	post = models.ForeignKey(HabitPost, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

class PostLike(HabitModel):
	post = models.ForeignKey(HabitPost, on_delete=models.CASCADE)

	@staticmethod
	def get_post_total_likes(post):
		return len(PostLike.objects.filter(post=post))

	@staticmethod
	def get_post_users_who_liked(post):
		return PostLike.objects.filter(post=post).values_list('user', flat=True)


class CommentLike(HabitModel):
	comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)


	@staticmethod
	def get_comment_total_likes(post):
		return len(PostLike.objects.filter(post=post))



def generate_habit_events(track, dates, instance):

	#HabitEvent.objects.bulk_create([HabitEvent(track=track, date=d) for d in dates])

	for d in dates:
		print("generating habit event for user: ")
		print(instance.user)
		HabitEvent.objects.create(track=track, date_expected=d, user=instance.user)
	
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

		"""
		datetimes = instance.recurrences.occurrences(

			# might also want to add dtend for efficiency later

			dtstart=instance.start_date
		)
		dates = [dt.date() for dt in datetimes] #this removes the time from the datetime
		"""
		print("GENERATING EVENTS FOR")
		print(instance.user)
		print("AUTOMATICALLY")

		dates = instance.get_dates()
		generate_habit_events(track=instance, dates=dates, instance=instance)


#POST SAVE DIDNT WORK AFTER I MADE POST CREATE VIEW 

# TODO Do something if today isn't a valid day to post, or limit the option to post from before this step
@receiver(post_save, sender=HabitPost, dispatch_uid="connect_habit_event_foreign_key_to_this_post")
def post_save_habit_posts(sender, instance, created, *args, **kwargs):

	if created:
		print("postsave habit posts the user is: ")
		print(instance.user)
		print(instance.slug)
		print(User)
		print("instance is: ")
		print(instance)
		event = HabitEvent.objects.filter(user=instance.user).filter(track=instance.track).filter(date_expected=instance.timestamp.date()).first()
		print(event)
		if event == None:
			print("##############################################################################################")
			print("*********************** NO POST EXPECTED FOR TODAY SO THIS IS AN ERROR THAT NEEDS TO BE FIXED")
			print("##############################################################################################")
		event.post = instance

		event.save() #this will save only the event column instead of the entire row
		print(event.post)
		print(event)
		event = HabitEvent.objects.filter(user=instance.user).filter(track=instance.track).filter(date_expected=instance.timestamp.date()).first()
		print(event.post)
		print(event)

