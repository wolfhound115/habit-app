from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import HabitPost, HabitTrack
from .forms import HabitPostModelForm, HabitTrackModelForm
from profiles.models import Profile


# CRUD: CREATE READ UPDATE DELETE
# GET -> Retrieve/List
# POST -> Create/Update/Delete


#CREATE

def habit_post_create_view(request):
	# create object
	# ? use a form
	form = HabitPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print(form.cleaned_data)
		#can do obj = form.save(commit=False) to modify data like 
		#obj.title = form.cleaned_data.get("title") + "0"
		#obj.save()
		form.save() 
		form = HabitPostModelForm()


	template_name = 'posts/form.html'
	context = {'form': form}
	return render(request, template_name, context)

def habit_track_create_view(request):
	# create object
	# ? use a form
	form = HabitTrackModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		print(form.cleaned_data)
		#can do obj = form.save(commit=False) to modify data like 
		#obj.title = form.cleaned_data.get("title") + "0"
		#obj.save()
		form.save() 
		form = HabitTrackModelForm()

	template_name = 'tracks/form.html'
	context = {'form': form}
	return render(request, template_name, context)

#RETRIEVE

def habit_post_list_view(request):
	# list out objects
	# could be search
	# latermight want to filter to only people you are following?
	#qs = HabitPost.objects.all() # python list

	qs = HabitPost.objects.filter(user=request.user)
	print(request.user)
	print(qs)
	template_name = 'posts/posts-grid.html'
	context = {'object_list': qs}
	return render(request, template_name, context)

def habit_track_list_view(request):
	# list out objects
	# could be search
	# latermight want to filter to only people you are following?
	#qs = HabitPost.objects.all() # python list

	qs = HabitTrack.objects.filter(user=request.user)
	print(request.user)
	print(qs)
	template_name = 'tracks/tracks-grid.html'
	context = {'object_list': qs}
	return render(request, template_name, context)



#def habit_post_detail_view(request, url_user, url_slug): #need to figure out better way of getting user specific data
def habit_post_detail_view(request, url_slug):

	qs = HabitPost.objects.filter(slug=url_slug)

	#print("hello hello" + HabitPost.objects.filter(user=url_user))
	obj = get_object_or_404(qs, slug=url_slug)
	template_name = 'posts/detail.html'
	context = {"object": obj}
	return render(request, template_name, context)

# UPDATE

def habit_post_update_view(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'posts/update.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)


# DELETE

def habit_post_delete_view(request, url_slug):
	obj = get_object_or_404(HabitPost, slug=url_slug)
	template_name = 'posts/delete.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)
	