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


class HabitTrackModelForm(forms.ModelForm):

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
		if timezone_corrected_start_date.date() < timezone_corrected_now.date():
			raise forms.ValidationError("The date cannot be in the past!")
		return timezone_corrected_start_date



class HabitPostEditModelForm(forms.ModelForm):
	class Meta:
		model = HabitPost
		fields = ['description', 'image']





class HabitPostModelForm(forms.ModelForm):

	#overriding so track_name is displayed rather than using __str__ representation of the name
	class TrackModelChoiceField(forms.ModelChoiceField):
		def label_from_instance(self, obj):
			return obj.track_name


	track = TrackModelChoiceField(queryset=None, to_field_name='track_name')
	description = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = HabitPost
		fields = ['track', 'description', 'image']

	def __init__(self, user, *args, **kwargs):

		super(HabitPostModelForm, self).__init__(*args, **kwargs)

		events_needing_post_today = HabitEvent.objects.filter(user=user, date_expected=date.today(), post__isnull=True)

		#get all the ids of tracks for events needing post today then filter tracks for only those ids
		track_ids = HabitEvent.objects.filter(user=user, date_expected=date.today(), post__isnull=True).values_list('track', flat=True)
		
		#this is the original faulty set
		tracks_needing_post_today = HabitTrack.objects.filter(id__in=track_ids)

		#get track ids of any track that has events owned by this user without a post yet
		track_ids_2 = HabitEvent.objects.filter(user=user, post__isnull=True).values_list('track', flat=True)


		user_tracks = HabitTrack.objects.filter(user=user)
		filtered_user_tracks = user_tracks
		for t in user_tracks:
			if not HabitEvent.objects.filter(user=user, track=t, date_expected=t.get_timezone_corrected_datetime_now().date(), post__isnull=True).exists():
				print("Excluding ", t.track_name, " with track specific time of ", t.get_timezone_corrected_datetime_now(), "from the list of options")
				filtered_user_tracks = filtered_user_tracks.exclude(pk=t.pk)
			else:
				print("Including ", t.track_name, " with track specific time of ", t.get_timezone_corrected_datetime_now(), "in the list of options")

		self.fields['track'].queryset = filtered_user_tracks #tracks_needing_post_today


