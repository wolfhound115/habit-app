from django import forms

from datetime import date, datetime

from .models import HabitPost, HabitTrack, HabitEvent, PostComment

from django.contrib.admin.widgets import AdminDateWidget

from django.utils import timezone

from timezone_field import TimeZoneFormField



class PostCommentModelForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['comment', 'parent', 'post']
		widgets = {
            'comment': forms.Textarea(
                attrs={'placeholder': 'Add a comment...'}),
        }

#class CommentLike:
"""
 class PostCommentReplyModelForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['comment']
		widgets = {
            'comment': forms.Textarea(
                attrs={'placeholder': 'Add a comment...'}),
        }
"""

class HabitTrackModelForm(forms.ModelForm):

	#timezone = TimeZoneFormField(display_GMT_offset=True) this doesnt work in the current update of django-timezone-field
	class Meta:
		model = HabitTrack
		fields = ['track_name', 'description', 'cover_image', 'timezone', 'start_date', 'recurrences']
		widgets = {
		    'start_date': AdminDateWidget(),
			}



	#note that fields are cleaned in order so they wont appear in cleaned data until the previous field has been cleaned
	def clean_timezone(self):
		timezone = self.cleaned_data['timezone']
		print(timezone)
		return timezone


	def clean_start_date(self):
		print(self.cleaned_data['timezone'])
		start_date = self.cleaned_data['start_date']
		track_timezone = self.cleaned_data['timezone']
		timezone_corrected_start_date = track_timezone.localize(start_date.replace(tzinfo=None))
		timezone_corrected_now = datetime.now(track_timezone)
		#print(timezone_corrected_start_date, timezone_corrected_start_date.date(), timezone_corrected_now, timezone_corrected_now.date(), timezone_corrected_start_date.date() < timezone_corrected_now.date())
		print("testing if ", start_date, " corrected to timezone ", track_timezone, " to be ", timezone_corrected_start_date, " has a date (ignoring time) before ", timezone_corrected_now)
		if timezone_corrected_start_date.date() < timezone_corrected_now.date():
			raise forms.ValidationError("The date cannot be in the past!")
		return timezone_corrected_start_date



class HabitPostEditModelForm(forms.ModelForm):
	class Meta:
		model = HabitPost
		fields = ['title', 'description', 'image']





class HabitPostModelForm(forms.ModelForm):
	class Meta:
		model = HabitPost
		fields = ['track', 'title', 'description', 'image']

	def __init__(self, user, *args, **kwargs):

		super(HabitPostModelForm, self).__init__(*args, **kwargs)

		events_needing_post_today = HabitEvent.objects.filter(user=user, date_expected=date.today(), post__isnull=True)
		
		print(date.today())
		print(user)
		print(HabitEvent.objects.filter(user=user))


		#tracks_today = HabitTrack.objects.filter(HabitEvent_set__user=user, HabitEvent_set__date_expected=date.today(), HabitEvent_set__post__isnull=True)
		#print(tracks_today)

		#get all the ids of tracks for events needing post today then filter tracks for only those ids
		track_ids = HabitEvent.objects.filter(user=user, date_expected=date.today(), post__isnull=True).values_list('track', flat=True)
		tracks_needing_post_today = HabitTrack.objects.filter(id__in=track_ids)

		print("These tracks should be listed in the dropdown: ")
		print(tracks_needing_post_today)

		#get track ids of any track that has events owned by this user without a post yet
		track_ids_2 = HabitEvent.objects.filter(user=user, post__isnull=True).values_list('track', flat=True)




		self.fields['track'].queryset = tracks_needing_post_today


		#self.fields['media'].queryset  = unused_files


		# not sure if it makes sense to do this because editing an old post still limits track options to those available for that day
"""
		instance = kwargs.get("instance")
		if instance:
			if instance.track:
				current_track = 
				self.fields.['track'] = 
				"""
"""
		instance = kwargs.get("instance")
        if instance:
            if instance.media:
                # if we're using this form to edit a post instance, we'll do this
                current_file = File.objects.filter(pk=instance.media.pk) 
                unused_files = ( unused_files | current_file ) # combine querysets

		self.fields['media'].queryset  = unused_files
        # pre-fill the timezone for good measure
        self.fields['publish_date'].initial = timezone.now()
"""

