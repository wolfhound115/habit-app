from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import HabitPost


# CRUD: CREATE READ UPDATE DELETE
# GET -> Retrieve/List
# POST -> Create/Update/Delete


#CREATE

def habit_post_create_view(request):
	# create object
	# ? use a form
	template_name = 'habit_post_create.html'
	context = {'form': None}
	return render(request, template_name, context)

#RETRIEVE

def habit_post_list_view(request):
	# list out objects
	# could be search
	
	qs = HabitPost.objects.all() # python list
	template_name = 'habit_post_list.html'
	context = {'object_list': qs}
	return render(request, template_name, context)


def habit_post_detail_view(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'habit_post_detail.html'
	context = {"object": obj}
	return render(request, template_name, context)

# UPDATE

def habit_post_update_view(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'habit_post_update.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)


# DELETE

def habit_post_delete_view(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'habit_post_delete.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)
	