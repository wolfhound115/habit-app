from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

# Create your views here.

from .models import HabitPost, HabitTrack, HabitModel, HabitEvent, CommentLike, PostLike, PostComment
from .forms import HabitPostModelForm, HabitTrackModelForm, PostCommentModelForm
from profiles.models import ProfileFollow, Profile
#from profiles.models import Profile
from django.conf import settings

from datetime import date

from django.contrib.auth import get_user_model

from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.edit import FormView



from django.views.decorators.http import require_GET, require_POST

from django.http import Http404
from django.core.paginator import Paginator



#This is so I can print the CSRF token to verify stuff manually
from django.middleware.csrf import get_token




from .models import get_likes_formatted



import json

# CRUD: CREATE READ UPDATE DELETE
# GET -> Retrieve/List
# POST -> Create/Update/Delete

#CREATE
#User = settings.AUTH_USER_MODEL





def generate_profile_context(request, url_username):
	print("url username to generate profile context is:")
	print(url_username)
	print("*******")

	new_post_url = reverse('new-post')
	profile_user = get_user_model().objects.filter(username=url_username).first()
	total_posts_made, total_posts_missed, overall_longest_streak = HabitTrack.get_user_habit_stats(profile_user)

	followers_count = ProfileFollow.get_profile_total_followers(profile_user.user_profile) + 200
	following_count = ProfileFollow.get_profile_total_followees(profile_user.user_profile) + 200



	if request.user == profile_user:
		checkins_expected = HabitEvent.count_check_ins_expected_today(profile_user)

	else:
		checkins_expected = None

	context = { 'profile_user': profile_user,
		     	'total_posts_made': total_posts_made,
	     		'total_posts_missed': total_posts_missed,
	     		'overall_longest_streak': overall_longest_streak,
	     		'new_post_url': new_post_url,
	     		'checkins_expected': checkins_expected,
	     		'following_count': following_count,
	     		'followers_count': followers_count,

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



def ProfileFollowToggle(request):
	user = request.user
	print("Profile Follow Toggle")
	if request.method == 'POST':
		profile_user_id = request.POST['profile_user_id'] #we get this post_id from our AJAX/Jquery
		profile_user = get_object_or_404(get_user_model(), id=profile_user_id)

		profile = profile_user.user_profile

		profile.followers.filter(follower=user.user_profile).exists()
		print("pre _followed")
		_followed = profile.followers.filter(follower=user.user_profile).exists() # return True/False
		print(_followed)
		if _followed:
			existing_profile_follow = profile.followers.filter(follower=user.user_profile)

			existing_profile_follow.delete()
			print("removed follow by " + user.__str__() + " on account " + profile_user.__str__())
		else:
			print("else")
			new_profile_follow = profile.followers.create(follower=user.user_profile)
			profile.followers.add(new_profile_follow)
			print("added follow by " + user.__str__() + " on account " + profile_user.__str__())
	print("finished conditionals in ProfileFollowToggle ")
	new_total_followers = ProfileFollow.get_profile_total_followers(profile)
	#if new_total_post_likes == 0:
	#	new_total_post_likes = ''

	_followed = not _followed
	return JsonResponse({	'followed': _followed,
							'new_total_followers': new_total_followers,
						})


def PostLikeToggle(request):


	print("POST LIKE TOGGLE TOKEN")
	print("POST LIKE TOGGLE TOKEN")
	print("POST LIKE TOGGLE TOKEN")

	print("POST LIKE TOGGLE TOKEN")
	print(get_token(request))


	user = request.user
	print("PostLikeToggle was used")
	if request.method == 'POST':
		post_id = request.POST['post_id'] #we get this post_id from our AJAX/Jquery
		post = get_object_or_404(HabitPost, id=post_id)
		print("pre _liked")
		_liked = post.post_likes.filter(user=user).exists() # return True/False
		print(_liked)
		if _liked:
			existing_post_like = post.post_likes.get(user=user)
			#post.post_likes.remove(existing_post_like)
			existing_post_like.delete()
			print("removed like by " + user.__str__() + " on post " + post.__str__())
		else:
			print("else")
			new_post_like = post.post_likes.create(user=user)
			post.post_likes.add(new_post_like)
			print("added like by " + user.__str__() + " on post " + post.__str__())
	print("finished conditionals in postliketoggle ")
	new_total_post_likes = PostLike.get_post_total_likes(post)
	#if new_total_post_likes == 0:
	#	new_total_post_likes = ''
	new_total_post_likes = get_likes_formatted(new_total_post_likes)


	post_like_button_text_id = "" + post_id + "-like-btn-txt"
	total_post_likes_id = "" + post_id + "-total-post-likes"


	_liked = not _liked
	return JsonResponse({	'liked': _liked,
							'new_total_post_likes': new_total_post_likes,
							'post_id': post_id,
							'post_like_button_text_id': post_like_button_text_id,
							'total_post_likes_id': total_post_likes_id,
						})

def CommentLikeToggle(request):
	user = request.user
	print("CommentLikeToggle was used")
	if request.method == 'POST':
		comment_id = request.POST['comment_id'] #we get this post_id from our AJAX/Jquery
		comment = get_object_or_404(PostComment, id=comment_id)
		print("pre _liked")
		_liked = comment.comment_likes.filter(user=user).exists() # return True/False
		print(_liked)
		if _liked:
			existing_comment_like = comment.comment_likes.get(user=user)
			#post.post_likes.remove(existing_post_like)
			existing_comment_like.delete()
			print("removed like by " + user.__str__() + " on comment " + comment.__str__())
		else:
			print("else")
			new_comment_like = comment.comment_likes.create(user=user)
			comment.comment_likes.add(new_comment_like)
			print("added like by " + user.__str__() + " on comment " + comment.__str__())
	print("finished conditionals in commentliketoggle ")
	new_total_comment_likes = CommentLike.get_comment_total_likes(comment)
	#if new_total_comment_likes == 0:
	#	new_total_comment_likes = ''
	new_total_comment_likes = get_likes_formatted(new_total_comment_likes)

	comment_like_button_text_id = "" + comment_id + "-like-btn-txt"
	total_comment_likes_id = "" + comment_id + "-total-comment-likes"

	_liked = not _liked
	print("comment like button text id is: " + comment_like_button_text_id)
	return JsonResponse({	'liked': _liked,
							'new_total_comment_likes': new_total_comment_likes,
							'comment_id': comment_id,
							'comment_like_button_text_id': comment_like_button_text_id,
							'total_comment_likes_id': total_comment_likes_id
						})



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

		return HttpResponseRedirect(request.path)

	profile_context = generate_profile_context(request, request.user.username)
	template_name = 'posts/form.html'
	context = {	'form': form,
				'create_view': '1',
				**profile_context

	}
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

		return HttpResponseRedirect(request.path)


	#todo: need to make sure only logged in users can see this page
	profile_context = generate_profile_context(request, request.user.username)
	print(profile_context)
	template_name = 'tracks/form.html'
	context = {	'form': form,
				'create_view': '1',
				**profile_context
	}
	return render(request, template_name, context)

#RETRIEVE

class NewsfeedView(ListView):
    model = HabitPost
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'newsfeed/newsfeed2.html'



    #Not sure if this method is needed or not...
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    	context = super().get_context_data(**kwargs)
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print("WE ARE DOING THE GET CONTEXT DATA THING")
    	print(get_token(self.request))
    # Add in the publisher
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



	#TODO this should be tracks/tracksgrid but it works fine for now
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

	print("hi this is the request.post below:")
	print(request.POST)

	qs = HabitPost.objects.filter(user__username=url_username, slug=url_slug)
	post = get_object_or_404(qs, user__username=url_username, slug=url_slug)
	template_name = 'posts/post-detail.html'
	profile_context = generate_profile_context(request, url_username)



	user = request.user
	post_liked_by_user = post.post_likes.filter(user=user).exists()
	form = PostCommentModelForm(request.POST or None) #, user=request.user)
	if form.is_valid():
		print("this is the cleaned form data: ")
		print(form.cleaned_data)
		
		form_obj = form.save(commit=False) #this way we can modify things before we save
		form_obj.user = request.user #now the blogposts are associated with the logged in user!
		form_obj.post = post
		print("before conditional")
		print(form_obj)
		print(form_obj.parent)
		print(form_obj)
		if form_obj.parent:
			print("after conditional")
			print(form_obj.parent)
			#form_obj.parent = post.comments.get(id = form_obj.parent)
			print(form_obj.parent)
		form_obj.save()
		form = PostCommentModelForm()
		return HttpResponseRedirect(request.path)
	else:
		print("form is not valid")
		print(form.errors)



	user_comment_likes = post.post_likes.filter(id=request.user.id).exists()
	context = { "post": post,
				"form": form,
				"post_liked_by_user": post_liked_by_user,
				**profile_context
			}
	return render(request, template_name, context)










"""
TRYING TO GET THE INFINITE SCROLLING TO WORK WITH SENTINELS THIS TIME


"""


def is_ajax(request):
    """
    This utility function is used, as `request.is_ajax()` is deprecated.

    This implements the previous functionality. Note that you need to
    attach this header manually if using fetch.
    """

    print("testing is_ajax")
    print("testing is_ajax")
    print("testing is_ajax")
    print(request.META.get("HTTP_X_REQUESTED_WITH"))
    print(request.META.get("HTTP-X-REQUESTED-WITH"))
    print("testing is_ajax")
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest" or request.META.get("HTTP-X-REQUESTED-WITH") == "XMLHttpRequest"



def post_list(request):
    """
    List view for posts.
    """
    form = PostCommentModelForm(request.POST or None) #, user=request.user)

    if form.is_valid():
    	print(form)
    	print(form)
    	print(form)
    	print(form)

    	print("this is the cleaned form data: ")
    	print(form.cleaned_data)
    	form_obj = form.save(commit=False) #this way we can modify things before we save
    	form_obj.user = request.user #now the blogposts are associated with the logged in user!
    	#form_obj.post = post
    	print("before conditional")
    	print(form_obj)
    	print(form_obj.parent)
    	print(form_obj)
    	if form_obj.parent:
    		print("after conditional")
    		print(form_obj.parent)
    		#form_obj.parent = post.comments.get(id = form_obj.parent)
    		print(form_obj.parent)
    	form_obj.save()
    	form = PostCommentModelForm()
    	return HttpResponseRedirect(HabitPost.objects.get(pk=form_obj.post).get_absolute_url())
    else:
    	print("form is not valid")
    	print(form.errors)


    all_posts = HabitPost.objects.order_by('-pk').all()
    paginator = Paginator(all_posts, per_page=5)
    page_num = int(request.GET.get("page", 1))
    if page_num > paginator.num_pages:
        raise Http404
    posts = paginator.page(page_num)
    if is_ajax(request):
        return render(request, 'posts/_posts.html', {'posts': posts})
    return render(request, 'newsfeed/newsfeed.html', {'posts': posts})



def autocompleteModel(request):

	print("autocompleteModel")
	print("autocompleteModel")
	print("autocompleteModel")
	print("autocompleteModel")
	print("autocompleteModel")
	print(request.is_ajax())
	#if request.is_ajax():


	# FOR SOME REASON q IS ALWAYS EMPTY, AND THATS WHY search_qs GETS ALL USER NAMES SINCE THEY ALL CONTAIN ""
	print("hi it is ajax in autocomplete")
	print(request)
	q = request.GET.get('term', '').capitalize()
	print(q)
	print(get_user_model().objects.all())
	for user in get_user_model().objects.all():
		print(user.username)
		print(user.username == q)
	search_qs = get_user_model().objects.filter(username__icontains=q)
	results = []
	print(q)
	print(q)
	print(q)


	#the json stuff here is django 1.6 or older so this can be updated
	for r in search_qs:
		results.append(r.username)
	data = json.dumps(results)
	print(results)
	print(data)
	#else:
		#data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)




class AutoCompleteView(FormView):
	print("AutoCompleteView")
	print("AutoCompleteView")
	print("AutoCompleteView")

	print("AutoCompleteView")
	print("AutoCompleteView")
	print("AutoCompleteView")

	def get(self,request,*args,**kwargs):
		print("flag 0")
		data = request.GET
		username = data.get("term")
		User=get_user_model()
		if username:
			print("flag 1")
			users = User.objects.filter(username__icontains = username)
		else:
			print("flag 2")
			users = User.objects.all()
		results = []
		for user in users:
			print("flag 3")
			print("user for loop user is: " + user.__str__())
			user_json = {}
			user_json['id'] = user.id
			user_json['label'] = user.username
			user_json['value'] = user.username
			user_json['url'] = user.get_profile_url()
			results.append(user_json)
		data = json.dumps(results)
		mimetype = 'application/json'
		print("flag 4")
		return HttpResponse(data, mimetype)




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
	