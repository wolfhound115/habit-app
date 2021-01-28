from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Profile



User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthdate', 'profile_bio', 'profile_image') #Note that we didn't mention user field here.
        widgets = {
            'profile_bio':  forms.Textarea()
        }




    
    """
    #this should be unnecessary because we create profile for user as soon as user registers
    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
	"""
	
