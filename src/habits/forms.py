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
"""
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tracks_needing_post_today = HabitTrack.objects.filter(user=user, date_expected=)
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