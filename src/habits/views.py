from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import HabitPost, HabitTrack, HabitModel, HabitEvent
from .forms import HabitPostModelForm, HabitTrackModelForm
from profiles.models import Profile
from django.conf import settings

from datetime import date

from django.contrib.auth import get_user_model

from django.urls import reverse


# CRUD: CREATE READ UPDATE DELETE
# GET -> Retrieve/List
# POST -> Create/Update/Delete

#CREATE
User = settings.AUTH_USER_MODEL


def habit_post_create_view(request):
	# create object
	# ? use a form
	user = request.user
	form = HabitPostModelForm(user, request.POST or None, request.FILES or None) #, user=request.user)
	if form.is_valid():
		print(form.cleaned_data)
		#can do obj = form.save(commit=False) to modify data like 
		#obj.title = form.cleaned_data.get("title") + "0"
		#obj.save()
		obj = form.save(commit=False) #this way we can modify things before we save
		obj.user = request.user #now the blogposts are associated with the logged in user!
		obj.save()
		form = HabitPostModelForm(user)


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
		obj = form.save(commit=False) #this way we can modify things before we save
		obj.user = request.user #now the blogposts are associated with the logged in user!
		obj.save()
		form = HabitTrackModelForm()

	template_name = 'tracks/form.html'
	context = {'form': form}
	return render(request, template_name, context)

#RETRIEVE



def habit_post_list_view(request, url_username):
	# list out objects
	# could be search
	# latermight want to filter to only people you are following?
	#qs = HabitPost.objects.all() # python list

	qs = HabitPost.objects.filter(user__username=url_username)
	print(qs)
	profile_user = get_user_model().objects.filter(username=url_username).first()
	print(profile_user.first_name, profile_user.last_name)

	template_name = 'posts/posts-grid.html'
	new_post_url = reverse('new-post')
	print('new post url: ')
	print(new_post_url)

	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected(profile_user)
	else:
		checkins_expected = None
	profile_url = "/habit/" + url_username
	print(profile_url)
	context = {'object_list': qs, 'profile_url': profile_url, 'profile_user': profile_user, 'checkins_expected': checkins_expected, 'new_post_url': new_post_url}
	return render(request, template_name, context)

def habit_track_list_view(request, url_username):
	# list out objects
	# could be search
	# latermight want to filter to only people you are following?
	#qs = HabitPost.objects.all() # python list

	qs = HabitTrack.objects.filter(user__username=url_username)
	print(qs)
	profile_user = get_user_model().objects.filter(username=url_username).first()
	print(profile_user.first_name, profile_user.last_name)
	new_post_url = reverse('new-post')
	template_name = 'tracks/tracks-grid.html'

	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected(profile_user)
	else:
		checkins_expected = None
	profile_url = "/habit/" + url_username
	context = {'object_list': qs, 'profile_url': profile_url, 'profile_user': profile_user, 'checkins_expected': checkins_expected, 'new_post_url': new_post_url}
	return render(request, template_name, context)

def habit_track_detail_feed_view(request, url_slug, url_username):
	track = HabitTrack.objects.filter(user__username=url_username, slug=url_slug).first()
	
	qs = HabitPost.objects.filter(user=request.user, track=track)

	profile_user = get_user_model().objects.filter(username=url_username).first()
	template_name = 'posts/posts-feed.html'
	profile_url = track.get_profile_url()
	track_url = track.get_absolute_url()
	new_post_url = reverse('new-post')
	print(track_url)
	print("dates:")
	print(track.get_dates())
	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected(profile_user)
	else:
		checkins_expected = None
	context = {'object_list': qs, 'profile_url': profile_url, 'track_url': track_url, 'profile_user': profile_user, 'checkins_expected': checkins_expected, 'new_post_url': new_post_url}
	return render(request, template_name, context)



def habit_track_detail_grid_view(request, url_slug, url_username):
	track = HabitTrack.objects.filter(user__username=url_username, slug=url_slug).first()
	qs = HabitPost.objects.filter(user=request.user, track=track)

	profile_user = get_user_model().objects.filter(username=url_username).first()
	template_name = 'posts/posts-grid.html'
	profile_url = track.get_profile_url()
	track_url = track.get_absolute_url()
	new_post_url = reverse('new-post')
	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected(profile_user)
	else:
		checkins_expected = None
	context = {'object_list': qs, 'profile_url': profile_url, 'track_url': track_url, 'profile_user': profile_user, 'checkins_expected': checkins_expected, 'new_post_url': new_post_url}
	return render(request, template_name, context)



#def habit_post_detail_view(request, url_user, url_slug): #need to figure out better way of getting user specific data
def habit_post_detail_view(request, url_slug, url_username):

	qs = HabitPost.objects.filter(user__username=url_username, slug=url_slug)

	#print("hello hello" + HabitPost.objects.filter(user=url_user))
	obj = get_object_or_404(qs, user__username=url_username, slug=url_slug)
	template_name = 'posts/detail.html'
	context = {"object": obj}
	return render(request, template_name, context)

# UPDATE

def habit_post_update_view(request, url_slug, url_username):
	obj = get_object_or_404(HabitPost, user__username=url_username, slug=url_slug)
	template_name = 'posts/update.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)


# DELETE

def habit_post_delete_view(request, url_slug, url_username):
	obj = get_object_or_404(HabitPost, user__username=url_username, slug=url_slug)
	template_name = 'posts/delete.html'
	context = {"object": obj, 'form': None}
	return render(request, template_name, context)
	