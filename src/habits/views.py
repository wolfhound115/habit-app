from django.shortcuts import render

# Create your views here.

from .models import HabitPost

def habit_post_detail_page(request):
	obj = HabitPost.objects.get(id=1)
	template_name = 'habit_post_detail.html'
	context = {"object": obj}
	return render(request, template_name, context)