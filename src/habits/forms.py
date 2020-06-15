from django import forms

from .models import HabitPost

class HabitPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	description = forms.CharField(widget=forms.Textarea)


class HabitPostModelForm(forms.ModelForm):
	class Meta:
		model = HabitPost
		fields = ['title', 'slug', 'description', 'image', 'track']