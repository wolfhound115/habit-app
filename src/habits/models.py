from django.db import models
from django.conf import settings
from django.utils import timezone


from django.contrib.auth.models import AbstractUser

from recurrence.fields import RecurrenceField

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from datetime import date, datetime, timedelta

import os
import random

from timezone_field import TimeZoneField

# Create your models here.



User = settings.AUTH_USER_MODEL


#this is to avoid image filename overlaps and organize user file uploads
def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(50))
    return 'image/userphotos/{userid}/{randomstring}{ext}'.format(userid= instance.user.id, randomstring= randomstr, ext= file_extension)





def get_likes_formatted(likes):
	if not likes:
		return ""
	elif likes == 1:
		return "1 like"
	else:
		return "" + str(likes) + " likes"

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


class HabitModel(models.Model):
	user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)



class JustRecurrence(models.Model):
	recurrences = RecurrenceField(null=True)

		
#Similar to a facebook album could allow comments on the overall track aswell as individual posts
class HabitTrack(HabitModel):
	track_name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	description = models.CharField(max_length=2200)
	cover_image = models.ImageField(upload_to=photo_path, blank=False, null=True)
	recurrences = RecurrenceField(include_dtstart=False, null=False, blank=False)
	start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=False)
	end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=False)
	creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True) #just for sorting tracks made same day purposes
	timezone = TimeZoneField(default='America/Los_Angeles', blank=False, null=False) # defaults supported


	def get_num_posts_expected(self):
		return len(self.get_dates())

	def get_all_events(self):
		return HabitEvent.objects.filter(track=self)

	def get_num_posts_made(self):
		return len(self.get_all_events().filter(post__isnull=False))

	def get_post_events_missed(self):
		all_events = self.get_all_events()
		post_events_missed = all_events.filter(track=self, date_expected__lt=self.get_timezone_corrected_datetime_now().date(), post__isnull=True)
		return post_events_missed

	def get_num_posts_missed(self):
		return len(self.get_post_events_missed())


#this breaks if you delete a single event because then len(dates) and len(all_events) will not be the same
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


	def get_timezone_corrected_datetime_now(self):
		timezone_corrected_now = datetime.now(self.timezone)
		print(timezone_corrected_now)
		return timezone_corrected_now

	def is_post_expected_today(self):
		print(self.id, self.timezone)
		print(HabitEvent.objects.filter(user=self.user, track=self, date_expected=datetime.now(self.timezone).date(), post__isnull=True))

	@staticmethod
	def count_check_ins_expected_today(user):
		total_check_ins_expected = 0
		for track in HabitTrack.objects.filter(user=user):
			total_check_ins_expected += HabitEvent.objects.filter(user=user, track=track, date_expected=track.get_timezone_corrected_datetime_now().date(), post__isnull=True).count()
		return total_check_ins_expected


	@staticmethod
	def get_user_habit_stats(user):
		tracks = HabitTrack.objects.filter(user=user)
		total_posts_made = 0
		total_posts_missed = 0
		overall_longest_streak = 0

		for t in tracks:
			total_posts_made += t.get_num_posts_made()
			total_posts_missed += t.get_num_posts_missed()
		return total_posts_made, total_posts_missed, overall_longest_streak

	def save(self, *args, **kwargs):
		""" Add Slug creating/checking to save method. """
		slug_save(self) # call slug_save, listed below
		super(HabitTrack, self).save(*args, **kwargs)

	def __str__(self):
		#self.is_post_expected_today()
		return self.id.__str__() + " " + self.track_name + " " + self.creation_date.__str__()

	def get_dates(self):
		print(self.recurrences)
		datetimes = self.recurrences.between(
			# this is the only way to allow start and end dates to be included ONLY if the days also fit the recurrence pattern
			# otherwise they are included by default or not included even if the days fit the pattern
			self.start_date - timedelta(days=1),
			self.end_date + timedelta(days=1),
			dtstart=self.start_date - timedelta(days=1),
			dtend=self.end_date + timedelta(days=1),
		)
		dates = [dt.date() for dt in datetimes]
		return dates

	class Meta:
		ordering = ['-start_date', '-creation_date'] #the order of these is the order that posts will be sorted by

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


def get_age_from_timestamp(timestamp, shorten):
	short_form, long_form = 0, 1
	if shorten:
		short_form, long_form = 1, 0

	age = timezone.now() - timestamp
	age_in_sec = int(age.total_seconds())

	def plurify(val):
		if val == 1:
			return ""
		else:
			return "S"

	if age_in_sec < 60:
		return str(int(age_in_sec)) + "s"*short_form + (" SECOND" + plurify(age_in_sec) + " AGO")*long_form
	age_in_min = age_in_sec // 60
	if age_in_min < 60:
		return str(age_in_min) + "m"*short_form + (" MINUTE" + plurify(age_in_min) + " AGO")*long_form
	age_in_hour = age_in_min // 60
	if age_in_hour < 24:
		return str(age_in_hour) + "h"*short_form + (" HOUR" + plurify(age_in_hour) + " AGO")*long_form
	age_in_day = age_in_hour // 24
	if age_in_day < 7:
		return str(age_in_day) + "d"*short_form + (" DAY" + plurify(age_in_day) + " AGO")*long_form
	age_in_week = age_in_day // 7
	#if age_in_day < 31:
	return str(age_in_week) + "w"*short_form + (" WEEK" + plurify(age_in_week) + " AGO")*long_form

class HabitPost(HabitModel):

	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=100, null=True)
	description = models.CharField(max_length=2200)
	image = models.ImageField(upload_to=photo_path, blank=False, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	track = models.ForeignKey(HabitTrack, null=True, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		""" Add Slug creating/checking to save method. """
		slug_save(self) # call slug_save, listed below
		super(HabitPost, self).save(*args, **kwargs)


	class Meta:
		ordering = ['-timestamp'] #the order of these is the order that posts will be sorted by

	def __str__(self):
		return self.track.__str__() + " " + self.timestamp.date().__str__()

	def get_absolute_url(self):
		return f"{self.user.get_profile_url()}/posts/{self.slug}"

	def get_edit_url(self):
		return f"{self.get_absolute_url()}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url()}/delete"

	def get_age(self):
		return get_age_from_timestamp(self.timestamp, shorten=False)

	def get_num_post_likes(self):
		return len(self.post_likes.all())

	def get_num_post_comments(self):
		return len(self.comments.all())

	def get_post_likes_formatted(self):
		print(self.get_comments_preview())
		return get_likes_formatted(len(self.post_likes.all()))


	#returns the last 2 comments made on the post most recently
	def get_comments_preview(self):
		return self.comments.all().order_by('-timestamp')[:2:-1]

	def has_many_comments(self):
		return len(self.comments.all()) >= 3


	def get_post_specific_streak(self):
		dates = self.track.get_dates()
		all_previous_events = self.track.get_all_events().filter(date_expected__lte=self.post_event.date_expected)
		streak = 0
		skipped_previous = True
		for d in dates:
			if d > self.post_event.date_expected:
				return streak
			if all_previous_events.get(date_expected=d).post is not None:
				streak += 1
				print(streak)
				skipped_previous = False
			elif skipped_previous is False:
				skipped_previous = True
			else:
				streak = 0
		return streak


	def get_post_num(self):
		return len(self.track.get_all_events().filter(date_expected__lte=self.post_event.date_expected))


	def get_total_posts_expected_num(self):
		return len(self.track.get_all_events())


class HabitEvent(HabitModel):
	track = models.ForeignKey(HabitTrack, on_delete=models.CASCADE, null=False)
	date_expected = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False) #make null=false later
	post = models.OneToOneField(HabitPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="post_event")

	def __str__(self):
		return self.date_expected.strftime("%m/%d/%Y") + self.track.__str__()

	def count_check_ins_expected_today(user):
		events_needing_post_today = HabitEvent.objects.filter(user=user, date_expected=timezone.now().date(), post__isnull=True)
		return len(events_needing_post_today)




#remove the blank=trues on the timestamps??? not sure why database is having issues
class PostComment(HabitModel):
	comment = models.TextField(max_length=300)
	post = models.ForeignKey(HabitPost, on_delete=models.CASCADE, related_name='comments')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		ordering = ['timestamp'] #the order of these is the order that comments will be sorted by
		
	def __str__(self):
		s = self.pk.__str__() + self.user.__str__()
		if self.parent is not None:
			s += " REPLY TO " + self.parent.__str__()
		s += " " + self.comment.__str__()

		s += " " + self.timestamp.__str__()
		return s



	def get_age(self):
		return get_age_from_timestamp(self.timestamp, shorten=True)


	def get_comment_likes_formatted(self):
		return get_likes_formatted(len(self.comment_likes.all()))



class PostLike(HabitModel):
	post = models.ForeignKey(HabitPost, on_delete=models.CASCADE, related_name='post_likes')
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		ordering = ['timestamp'] #the order of these is the order that comments will be sorted by

	@staticmethod
	def get_post_total_likes(post):
		return len(PostLike.objects.filter(post=post))

	@staticmethod
	def get_post_users_who_liked(post):
		return PostLike.objects.filter(post=post).values_list('user', flat=True)




class CommentLike(HabitModel):
	comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comment_likes')
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		ordering = ['timestamp'] #the order of these is the order that comments will be sorted by

	@staticmethod
	def get_comment_total_likes(comment):
		return len(CommentLike.objects.filter(comment=comment))



def generate_habit_events(track, dates, instance):

	#HabitEvent.objects.bulk_create([HabitEvent(track=track, date=d) for d in dates])

	for d in dates:
		print("generating habit event for user: ")
		print(instance.user)
		HabitEvent.objects.create(track=track, date_expected=d, user=instance.user)
	


@receiver(post_save, sender=HabitTrack, dispatch_uid="generate_empty_habit_events")
def post_save_habit_tracks(sender, instance, created, *args, **kwargs):
	print("*******")
	print("post save habit tracks reliever")
	if created:

		
		print("GENERATING EVENTS FOR")
		print(instance.user)
		print("AUTOMATICALLY")

		dates = instance.get_dates()
		generate_habit_events(track=instance, dates=dates, instance=instance)



@receiver(post_save, sender=HabitPost, dispatch_uid="connect_habit_event_foreign_key_to_this_post")
def post_save_habit_posts(sender, instance, created, *args, **kwargs):

	if created:
		print("postsave habit posts the user is: ")
		print(instance.user)
		print(instance.slug)
		print("instance is: ")
		print(instance)

		timezone_corrected_date_expected=instance.track.get_timezone_corrected_datetime_now().date()
		incorrect_event = HabitEvent.objects.filter(user=instance.user).filter(track=instance.track).filter(date_expected=instance.timestamp.date()).first()
		event = HabitEvent.objects.filter(user=instance.user).filter(track=instance.track).filter(date_expected=timezone_corrected_date_expected).first()

		print(event)
		if event == None:
			print("##############################################################################################")
			print("*********************** NO POST EXPECTED FOR TODAY SO THIS IS AN ERROR IF IT OCCURS ##########")
			print("##############################################################################################")
		event.post = instance
		event.save() #this will save only the event column instead of the entire row


