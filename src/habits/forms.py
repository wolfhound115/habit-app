from django import forms

from .models import HabitPost, HabitTrack

from django.contrib.admin.widgets import AdminDateWidget



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
		fields = ['title', 'slug', 'description', 'image', 'track']
