from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import HabitPost, HabitTrack, HabitModel, HabitEvent
from .forms import HabitPostModelForm, HabitTrackModelForm, PostCommentModelForm
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
def generate_profile_context(request, url_username):

	new_post_url = reverse('new-post')
	profile_user = get_user_model().objects.filter(username=url_username).first()
	profile_url = profile_user.get_profile_url()
	total_posts_made, total_posts_missed, overall_longest_streak = HabitTrack.get_user_habit_stats(profile_user)



	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected_today(profile_user)

	else:
		checkins_expected = None

	context = { 'profile_user': profile_user,
				'profile_url': profile_url,
		     	'total_posts_made': total_posts_made,
	     		'total_posts_missed': total_posts_missed,
	     		'overall_longest_streak': overall_longest_streak,
	     		'new_post_url': new_post_url,
	     		'checkins_expected': checkins_expected,

	}
	print(context)
	return context

def generate_track_context(request, url_slug, url_username):
	track = HabitTrack.objects.filter(user__username=url_username, slug=url_slug).first() #TODO change to get()


	track_desc = track.description
	qs = HabitPost.objects.filter(user__username=url_username, track=track)
	track_name = track.track_name
	track_url = track.get_absolute_url()
	streak_this_track, longest_streak_this_track = track.get_streaks()
	num_posts_made = track.get_num_posts_made()
	num_posts_missed = track.get_num_posts_missed()
	num_posts_expected = track.get_num_posts_expected()

	context = { 'object_list': qs,
				'streak_this_track': streak_this_track,
	     		'longest_streak_this_track': longest_streak_this_track,
	     		'num_posts_made': num_posts_made,
	     		'num_posts_missed': num_posts_missed,
	     		'num_posts_expected': num_posts_expected,
	     		'track_url': track_url,
	     		'track_name': track_name,
	     		'track_desc': track_desc

	}
	print(context)
	return context


def generate_all_posts_context(request, url_username):
	qs = HabitPost.objects.filter(user__username=url_username)
	context = { 'object_list': qs,
	}
	print("context", context)
	return context

def generate_all_tracks_context(request, url_username):
	qs = HabitTrack.objects.filter(user__username=url_username)
	context = { 'object_list': qs,
	}
	print("context", context)
	return context

def habit_all_posts_list_view(request, url_username):
	# list out objects
	# could be search
	# latermight want to filter to only people you are following?
	#qs = HabitPost.objects.all() # python list

	template_name = 'posts/posts-grid.html'
	profile_context = generate_profile_context(request, url_username)
	posts_context = generate_all_posts_context(request, url_username)
	context = {	'template_name': template_name,
				**profile_context, 
				**posts_context
				} #merge two context dictionaries

	return render(request, template_name, context)

def habit_all_tracks_list_view(request, url_username):
	template_name = 'tracks/tracks-grid.html'
	profile_context = generate_profile_context(request, url_username)
	tracks_context = generate_all_tracks_context(request, url_username)
	context = {	'template_name': template_name,
				**profile_context, 
				**tracks_context
				} #merge two context dictionaries

	return render(request, template_name, context)



def habit_track_detail_grid_view(request, url_slug, url_username):

	template_name = 'posts/posts-grid.html'
	profile_context = generate_profile_context(request, url_username)
	track_context = generate_track_context(request, url_slug, url_username)
	context = {	'template_name': template_name,
				**profile_context, 
				**track_context
				} #merge two context dictionaries

	return render(request, template_name, context)

def habit_track_detail_feed_view(request, url_slug, url_username):
	
	template_name = 'posts/posts-feed.html'
	profile_context = generate_profile_context(request, url_username)
	track_context = generate_track_context(request, url_slug, url_username)
	context = {	'template_name': template_name,
				**profile_context, 
				**track_context
				} #merge two context dictionaries

	return render(request, template_name, context)





#def habit_post_detail_view(request, url_user, url_slug): #need to figure out better way of getting user specific data
def habit_post_detail_view(request, url_slug, url_username):

	qs = HabitPost.objects.filter(user__username=url_username, slug=url_slug)
	post = get_object_or_404(qs, user__username=url_username, slug=url_slug)
	template_name = 'posts/post-detail.html'
	profile_context = generate_profile_context(request, url_username)



	user = request.user
	form = PostCommentModelForm(request.POST or None) #, user=request.user)
	if form.is_valid():
		print(form.cleaned_data)
		
		form_obj = form.save(commit=False) #this way we can modify things before we save
		form_obj.user = request.user #now the blogposts are associated with the logged in user!
		form_obj.post = post
		form_obj.save()
		form = PostCommentModelForm()
		

	context = { "post": post,
				"form": form,
				**profile_context
			}
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
	