from django import forms

from datetime import date

from .models import HabitPost, HabitTrack, HabitEvent, PostComment

from django.contrib.admin.widgets import AdminDateWidget



class PostCommentModelForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['comment']
		widgets = {
            'comment': forms.Textarea(
                attrs={'placeholder': 'Add a comment...'}),
        }
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


	class Meta:
		model = HabitTrack
		fields = ['track_name', 'description', 'cover_image', 'start_date', 'recurrences']
		widgets = {
            'start_date': AdminDateWidget(),
        }

class HabitPostModelForm(forms.ModelForm):
	class Meta:
		model = HabitPost
		fields = ['title', 'description', 'image', 'track']

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

