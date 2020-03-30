from django.http import HttpResponse
from django.shortcuts import render



def home_page(request):
	my_title = "Hello World this is Habit!"
	return render(request, "hello_world.html", {"title": my_title})


def about_page(request):
	my_title = "About Habit: Building Habits bit by bit"
	return render(request, "hello_world.html", {"title": my_title})


def contact_page(request):
	my_title = "Contact Us!"
	return render(request, "hello_world.html", {"title": my_title})