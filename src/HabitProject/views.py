from django.http import HttpResponse
from django.shortcuts import render

from habits.models import HabitPost

#User = settings.AUTH_USER_MODEL not sure if i need this yet

### request is an HttpRequest object, views are responsible for returning an HttpResponse object
def home_page(request):
	my_title = "Habit@ - Where good habits grow, bit by bit"


	if request.user.is_authenticated:
		authenticated_user_content = "Hello " + request.user.username + ", welcome back!"
	else:
		authenticated_user_content = "Hello! Please log in for full access!"

	context = {"title": my_title, "authenticated_user_content": authenticated_user_content}


	return render(request, "home.html", context)


def about_page(request):
	my_title = "About Habit: Building Habits bit by bit"
	post = HabitPost.objects.filter(user=request.user).first()#filter(image!=None) #will probably need a post view that is passed in somehow isntead
	context = {"title": my_title, "post": post}
	return render(request, "instagram.html", context)


def contact_page(request):
	my_title = "Contact Us!"
	return render(request, "hello_world.html", {"title": my_title})