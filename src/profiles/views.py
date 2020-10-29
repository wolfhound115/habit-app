from django.shortcuts import render, redirect, reverse

from .models import Profile

from django.views.generic import UpdateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin



from .forms import EditProfileForm

# Create your views here.





#@method_decorator(login_required(login_url='/habit/login'), name='dispatch')
class EditProfileView(LoginRequiredMixin, UpdateView):
	form_class = EditProfileForm
	template_name = "profiles/edit-profile.html"


	def get_object(self):
		return get_object_or_404(Profile, user=self.request.user)

	def get_success_url(self, *args, **kwargs):
		return self.request.user.get_profile_url()