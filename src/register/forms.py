from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



User = get_user_model()

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ["email", "first_name", "last_name", "username", "password1", "password2"]
		unique_together = ('email', 'username')# probably unnecessary
		
	def save(self, commit=True):
		user = super (RegisterForm , self ).save(commit=False)
		user.is_staff = True

		if commit :
			user.save()
		return user
