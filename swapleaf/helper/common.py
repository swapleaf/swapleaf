from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User

from swapleaf.app.app_settings import SESSION_KEY, MESSAGE_SNIPPET_TEMPLATE
from swapleaf.app.account.models import SwapLeafEmailAddress
from swapleaf.app.friends.models import Friendship
from swapleaf.app.main.models import Notify

def remove_duplicate_object(l):
	return list(set(l))

def convert_queryset_to_list(obj_queryset):
	result = []
	if len(obj_queryset) != 0:
		for obj in obj_queryset:
			result.append(obj)
	return result

def get_user_login_object(request):
	if SESSION_KEY in request.session:
		user_id = request.session[SESSION_KEY]
		user = User.objects.filter(pk=user_id)
		if len(user) == 1:
			return user[0]
	return None

def generate_message(action,result,user_login):
	template_name = action + "_" + result
	snippet = render_to_string(MESSAGE_SNIPPET_TEMPLATE[template_name],{'user_login':user_login})
	return snippet

def handle_request_get_message(request):
	user_login = get_user_login_object(request)
	if "action" in request.GET and "result" in request.GET:	
		return  generate_message(request.GET['action'],request.GET['result'],user_login)
	else:
		if user_login:
			email_confirmation = SwapLeafEmailAddress.objects.filter(email=user_login.email)
			if len(email_confirmation) != 0:
				print email_confirmation[0].verified
				if email_confirmation[0].verified == False: 
					return generate_message("confirm_email","asking",user_login)
		return None

def get_user_autocomplete_data(request):
	user_login = get_user_login_object(request)
	# if user_login == None: 
	# 	return []
	if user_login == None:
		users = User.objects.exclude(is_staff=True)
	else:
		users = User.objects.exclude(pk=user_login.pk).exclude(is_staff=True)
	result = []
	for user in users:
		description = "People"
		if user_login != None and Friendship.objects.are_friends(user_login, user):
			description = "Partner" 
		result.append({
				'name': str(user.first_name + " " + user.last_name),
				#'icon': user.avatar.url,
				'description': description,
				'value': str(user.username), 
				'type': 'member'
		})
	return result

def get_autocomplete_data(request):
	return simplejson.dumps(get_user_autocomplete_data(request),indent=2)

def get_new_notify(request):
	user_login = get_user_login_object(request)
	if user_login:
		notifies = Notify.objects.filter(status="new",notify_to=user_login)
		return notifies
	return []

def check_identical_author(a1,a2):
	a1_words = a1.split()
	a2_words = a2.split()
	a1_words.sort()
	a2_words.sort()
	for i in range(0,len(a1_words)):
		a1_words[i] = a1_words[i].lower()
	for i in range(0,len(a2_words)):
		a2_words[i] = a2_words[i].lower()
	if a1_words == a2_words:
		return True
	return False