from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import HabitPost

def habit_post_detail_page(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'habit_post_detail.html'
	context = {"object": obj}
	return render(request, template_name, context)