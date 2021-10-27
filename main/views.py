from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from home.models import Post
from social_media.settings import AUTH_USER_MODEL
from users.models import User
import ast
from .templatetags import get_last
from .templatetags import typess
from .templatetags import convert_list
from .templatetags import dictio
from .templatetags import get_index


def home(req):
	return redirect("/home") 

def add_post(req):

	if(req.method=="POST"):
		username = req.POST.get('username')
		caps = req.POST.get('captions')

		path = req.FILES.getlist("images")

		done_Post = Post(username=username, image=path[0], caption=caps)
		done_Post.save()

		return redirect("/home")

	else:
		return HttpResponse("404 error !")


def profile(req, username):

	profile_user = User.objects.filter(username=username).first()

	all_users = [user.username for user in User.objects.all()]

	# PASSING ALL THE REPLIES TO THE TEMPALATE

	all_posts = Post.objects.all()
	ids = {} # it will store all replies with their UNIQUE ID 
	di = {} # it will store all post's replies iterating below

	for y in all_posts:
		if(len(y.replies)==0):
			pass
			
		else:
			di[y.sno] = ast.literal_eval(y.replies)
			
	# iterating our replies with their ids
	if(len(di)==0):
		ids = {}
	else:	
		# PASSING COMPLETE DICTIONARY WITH USERNAME WITH KEY VALUE OF REPLY AND ITS ID
		for first_dict_key, first_dict_val in di.items():
			for second_dict_key,second_dict_val in first_dict_val.items():
				for third_dict_key,third_dict_val in second_dict_val.items():
					ids[second_dict_key] = {third_dict_key:int(third_dict_val)}
					

	if(profile_user is not None):
		postss = Post.objects.filter(username=username)
		context = {'profile':profile_user, 'post':postss, 'all_users':all_users, 'ids':ids}
		return render(req, "main/profile.html", context)
	else:
		return render(req, "main/no_user.html")


def edit_profile(req):

	logged_user_data = User.objects.filter(username=req.user.username).first()	


	if(req.method=="POST"):
		
		profile_pic = req.POST.get('profile')
		fname = req.POST.get('fname')
		username = req.POST.get('username')
		email = req.POST.get('email')
		bio = req.POST.get('bio')

		path_of_image = req.FILES.getlist("profile")
	

		# putting this in try except block cuz if use doesn't want to update the image then he should not get any error	
		try:
			logged_user_data.profile_pic = path_of_image[0]
		except Exception as e:
			pass

		logged_user_data.fname = fname
		logged_user_data.username = username
		logged_user_data.email = email
		logged_user_data.bio = bio
		logged_user_data.save()

		# redirecting user to his profile page after editing the profile
		return redirect("/main/"+req.user.username)


	context = {'user':logged_user_data}

	return render(req, "main/edit.html")


def follow(req):

	f = None
	usern = None
	if(req.method=="POST"):
		logged_user = User.objects.filter(username=req.user.username).first()
		usern = req.POST.get("user-name")
		user_to_follow = User.objects.filter(username=usern).first()

		# updating the user's followers
		followers = None
		if(len(user_to_follow.followers)==0):
			followers = []
		else:
			followers = ast.literal_eval(user_to_follow.followers)

		if(len(logged_user.following)==0):
			f = []

		else:
			f = ast.literal_eval(logged_user.following)


		notifications = None # making this global to be used by every part
		if(usern not in f):
			f.append(usern)
			followers.append(logged_user.username)

			# sending notifications

			if(len(user_to_follow.notifications)==0):
				notifications = []
			else:
				notifications = ast.literal_eval(user_to_follow.notifications)
				# for limiting the notification's length
				if(len(notifications)>7):
					notifications.pop(0)

			notifications.append({logged_user.username + str(len(notifications)+1):{" has started following you.":""}})

			user_to_follow.notifications = str(notifications)
			user_to_follow.save()


		else:		
			f.remove(usern)	
			followers.remove(logged_user.username)

			# sending notifications

			if(len(user_to_follow.notifications)==0):
				notifications = []
			else:
				notifications = ast.literal_eval(user_to_follow.notifications)
				# for limiting the notification's length
				if(len(notifications)>7):
					notifications.pop(0)

			notifications.append({logged_user.username + str(len(notifications)+1):{" has unfollowed you.":""}})

			user_to_follow.notifications = str(notifications)
			user_to_follow.save()


		user_to_follow.followers = followers
		user_to_follow.save()

		logged_user.following = f
		logged_user.save()

	
	return redirect(f'/main/{usern}')