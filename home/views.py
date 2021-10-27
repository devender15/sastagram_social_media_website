from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from users.models import User
from .templatetags import dictio
from .templatetags import convert_dict
from .templatetags import get_index
import ast # importing this module for converting string dict to actual dict
import random
from .templatetags import get_last
from .templatetags import typess
from .templatetags import convert_list


def home(req):

	# updating the likes to the database
	all_posts = Post.objects.all()
	val = User.objects.all()
	
	current_loggedin_user = User.objects.get(username=req.user.username)

	# using ast module for converting string dictionary to actual dictionary

	# implementing some checks for if the user is a new user

	s = None

	if(len(current_loggedin_user.liked_posts)==0):
		s = {}
	else:
		s = ast.literal_eval(current_loggedin_user.liked_posts)

	dicti = s

	if(req.method=="POST"):
		likess = req.POST.get("likes")
		post_id = req.POST.get("postid")
		logged_user = req.POST.get("loggeduser")
	
		post_all = Post.objects.filter(sno=post_id).first()

		user_filtered = User.objects.filter(email=logged_user).first()
		# filtering out the user on whose post we are doing the event
		user_post = User.objects.filter(username=post_all).first()
			

		# logic for making storing record of that user has liked that post or not
		if(int(post_id) not in s):
			dicti[post_all.sno] = True

			# if the user has zero notifications
			b = None

			if(len(user_post.notifications)==0):
				b = []

			else:
				# sending notifications
				notifications_dict = ast.literal_eval(user_post.notifications)
				b = notifications_dict
				# limiting notifications to just max 7

				if(len(b)>7):
					b.pop(0)

				
			# sending with unique username cuz to avoid the overriding the values
			
			b.append({user_filtered.username + str(len(b)+1): {" has liked your post":str(post_all.image)}})


			user_post.notifications = str(b)
			user_post.save()

		else:

			check = s[int(post_id)]

			if(check==True):
				dicti[post_all.sno] = False
			else:
				dicti[post_all.sno] = True

				# if the user has zero notifications
				b = None

				if(len(user_post.notifications)==0):
					b = []
				else:
					# sending notifications
					notifications_dict = ast.literal_eval(user_post.notifications)
					b = notifications_dict
					# limiting notifications to just max 7
					
					if(len(b)>7):
						b.pop(0)

				# sending with unique username cuz to avoid the overriding the values
				
				b.append({user_filtered.username + str(len(b)+1): {" has liked your post":str(post_all.image)}})

				user_post.notifications = str(b)
				user_post.save()

		user_filtered.liked_posts = str(dicti)
		user_filtered.save()

		post_all.likes = likess
		post_all.save()
	
	# making this dictionary for storing the path of user profile images correponding to the username
	dt = {}

	all_usernames = []

	for i in val:
		dt[i.username] = i.profile_pic
		all_usernames.append(i.username)

		# PASSING ALL REPLIES TO THE TEMPLATE


	ids = {} # it will store all replies with their UNIQUE ID 
	di = {} # it will store all post's replies iterating below

	for y in all_posts:
		if(len(y.replies)==0):
			pass
		else:
			di[y.sno] = ast.literal_eval(y.replies)

	# print(di)

	# iterating our replies with their ids
	if(len(di)==0):
		ids = {}
	else:	
		# PASSING COMPLETE DICTIONARY WITH USERNAME WITH KEY VALUE OF REPLY AND ITS ID
		for first_dict_key, first_dict_val in di.items():
			for second_dict_key,second_dict_val in first_dict_val.items():
				for third_dict_key,third_dict_val in second_dict_val.items():
					ids[second_dict_key] = {third_dict_key:int(third_dict_val)}


	context = {"all_posts":all_posts, 'user_model':dt, 'username':dicti, 'all_names':all_usernames, 'ids':ids}

	return render(req, "home/homepage.html", context)

def post_comments(req):

	if(req.method=="POST"):
		comment = req.POST.get("comment")

		if(len(comment)==0):
			pass

		else:
			user = req.user
			post_sno = req.POST.get('postid')
			parentSno = req.POST.get('parentSno') 
			# fetching all user's username
			all_users = User.objects.all()

			ps = Post.objects.filter(sno=post_sno).first()

			# converting comments dictionary to actual dictionary
			s2 = None
			if(len(ps.comments)==0):
				s2 = {}
			else:
				s2 = ps.comments
				s2 = ast.literal_eval(s2)

			# converting replies dictionary to actual dictionary
			all_replies = None

			if(len(ps.replies)==0):
				all_replies = {}
			else:
				all_replies = ps.replies
				all_replies = ast.literal_eval(all_replies)

			comment_dict = s2
			reply_dict = all_replies

			length_of_dict = len(comment_dict)
			length_of_rep_dict = len(reply_dict)

			UNIQUE_COMMENT_ID = random.randint(0, 1000) + length_of_dict+1

			post_all = Post.objects.filter(sno=post_sno).first()
			user_post = User.objects.filter(username=post_all).first()


			if(parentSno==""):
				# adding an integer value to the keys for making them uniquely store in dictionary
				comment_dict[f"{user.username+str(int(length_of_dict)+1)}"] = {comment:UNIQUE_COMMENT_ID}
				ps.comments = str(comment_dict)
				ps.save()


				# SENDING NOTIFICATIONS


				if(user.username != user_post.username):
					# if the user has zero notifications
					b = None

					if(len(user_post.notifications)==0):
						b = []

					else:
						# sending notifications
						notifications_dict = ast.literal_eval(user_post.notifications)
						b = notifications_dict

						# limiting notifications to 8
						if(len(b)>7):
							b.pop(0)

					# sending with unique username cuz to avoid the overriding the values

					b.append({user.username + str(len(b)+1): {" has commented on your post":comment}})

					user_post.notifications = str(b)
					user_post.save()

				else:
					pass
			
				# messages.success(req, "Your comment has been posted successfully.")
			else:

				reply_dict[f"{user.username+str(int(length_of_rep_dict)+1)}"] = {comment:parentSno}
				ps.replies = str(reply_dict)
				ps.save()


				# send reply notification to only the owner of comment
				user_comment = None
				for userq,comm in comment_dict.items():
					for co,ids in comm.items():
						if(ids==int(parentSno)):
							for usersss in all_users:
								if usersss.username in userq:
									userq = usersss.username
									user_comment = userq

				if(user_comment==user_post.username):
					# if the user has zero notifications
					b = None

					if(len(user_post.notifications)==0):
						b = []

					else:
						# sending notifications
						notifications_dict = ast.literal_eval(user_post.notifications)
						b = notifications_dict

						if(len(b)>7):
							b.pop(0)

					# sending with unique username cuz to avoid the overriding the values

					b.append({user.username + str(len(b)+1): {" replied to your comment.":comment}})

					user_post.notifications = str(b)
					user_post.save()

				else:
					pass

	return redirect("/home")


def search(req):

	context = {}

	if(req.method=="POST"):
		query = req.POST.get('query')
		matched_user = User.objects.filter(username__icontains=query)
		context['users'] = matched_user
		context['query'] = query

	return render(req, 'home/search.html', context)