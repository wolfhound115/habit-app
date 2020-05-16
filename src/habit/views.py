from django.http import HttpResponse
from django.shortcuts import render




### request is an HttpRequest object, views are responsible for returning an HttpResponse object
def home_page(request):
	my_title = "Hello World this is Habit!"
	context = {"title": my_title}
	return render(request, "home.html", context)


def about_page(request):
	my_title = "About Habit: Building Habits bit by bit"
	return render(request, "about.html", {"title": my_title})


def contact_page(request):
	my_title = "Contact Us!"
	return render(request, "hello_world.html", {"title": my_title})