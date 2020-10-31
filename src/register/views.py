from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from profiles.models import Profile


# Create your views here.
def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			print("this is the cleaned registration form data: ")
			print(form.cleaned_data)
			user_obj=form.save()
			Profile.objects.create(user=user_obj)

			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/habit/edit-profile') #redirect to edit profile view isntead to add profile picture/ bio/ dob/ etc
	else:
		form = RegisterForm()

	return render(request, "register/register.html", {"form":form})




