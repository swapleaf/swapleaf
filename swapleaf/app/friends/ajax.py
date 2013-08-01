from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User

from swapleaf.helper.common import get_user_login_object
from swapleaf.app.main.models import Notify
from swapleaf.app.friends.models import FriendshipRequest, Friendship
from swapleaf.app.app_settings import NOTIFY_SNIPPET_TEMPLATE

import datetime
import user_streams

# When user make an add friend request, create FriendshipRequest object and set accepted to False
# Create Friendship object of both user if they are not created, and send notify to the receiver user
# Status: COMPLETE
# Note:
#		_user_add_request is the current login user who click add button to this view user
#		_user_receive_request is the current view user
@dajaxice_register
def invite_partner(request,username):
	user_add_request = get_user_login_object(request)
	user_receive_request = User.objects.get(username=username)
	try:
		fr = FriendshipRequest.objects.get(from_user=user_add_request,to_user=user_receive_request)
		fr.accepted = False
		fr.save()
	except:
		FriendshipRequest.objects.create(from_user=user_add_request,to_user=user_receive_request,message='')
	try:
		Friendship.objects.get(user=user_add_request)
	except Friendship.DoesNotExist:
		Friendship.objects.create(user=user_add_request)
	try:
		Friendship.objects.get(user=user_receive_request)
	except Friendship.DoesNotExist:
		Friendship.objects.create(user=user_receive_request)
	if len(Notify.objects.filter(notify_type='invite_partner',notify_to=user_receive_request,notify_from=user_add_request)) == 0:
		notify_type= 'invite_partner'
		notify = Notify.objects.create(notify_type=notify_type,notify_to=user_receive_request,notify_from=user_add_request,status='new',date=datetime.datetime.now(),content='')
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['invite_partner'],
									{
										'username': user_add_request.username,
										'first_name': user_add_request.first_name,
										'last_name': user_add_request.last_name,
										'notify_id':  notify.pk
									})
		notify.content = content
		notify.save()
	new_notify = len(Notify.objects.filter(notify_to=user_receive_request,status='new'))
	return simplejson.dumps({
								'new_notify': new_notify,
								'username':username,
								'firstname': user_receive_request.first_name,
								'lastname': user_receive_request.last_name
							})

# Not notify user when they are unfriend
@dajaxice_register
def delete_partner(request,username):
	user_login = get_user_login_object(request)
	user_view = User.objects.get(username=username)
	Friendship.objects.unfriend(user_login,user_view)
	user_login.get_profile().partners.remove(user_view)
	user_view.get_profile().partners.remove(user_login)
	return simplejson.dumps(
				{
					'username':username,
					'firstname': user_view.first_name,
					'lastname': user_view.last_name 
				})

@dajaxice_register
def accept_partner(request,username,notify_id): 
	user_add_request = User.objects.get(username=username)
	user_receive_request = get_user_login_object(request)
	fr = FriendshipRequest.objects.filter(from_user=user_add_request, to_user=user_receive_request)
	# In case user A click accept while the other user B already cancel the request
	# we handle by reload the page
	if len(fr) != 0:
		fr[0].accept()
		notify_type= 'accept_partner'
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['accept_partner'],
									{
										'username': user_receive_request.username,
										'first_name': user_receive_request.first_name,
										'last_name': user_receive_request.last_name,
									})
		notify = Notify.objects.create(notify_type=notify_type,notify_to=user_add_request,notify_from=user_receive_request,status='new',date=datetime.datetime.now(),content=content)
		notify.save()
		n = Notify.objects.get(pk=notify_id)
		n.notify_type = 'invite_partner_response_accept'
		new_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['invite_partner_response_accept'],
									{
										'username': user_add_request.username,
										'first_name': user_add_request.first_name ,
										'last_name': user_add_request.last_name,
									})
		n.content = new_content
		n.save()
		new_notify = len(Notify.objects.filter(notify_to=user_add_request,status='new'))
		user_add_request.get_profile().partners.add(user_receive_request)
		user_receive_request.get_profile().partners.add(user_add_request)
		return simplejson.dumps({	
									'new_notify':new_notify, 
									'notify_id': notify_id, 
									'new_content': new_content, 
									'username':username,
									'firstname': user_add_request.first_name,
									'lastname': user_add_request.last_name,
									'reload': "False"
								})
	else:
		return simplejson.dumps({'reload': "True"})

@dajaxice_register
def decline_partner(request,username,notify_id):
	user_add_request = User.objects.get(username=username)
	user_receive_request = get_user_login_object(request)
	fr = FriendshipRequest.objects.filter(from_user=user_add_request, to_user=user_receive_request, accepted=False)
	if len(fr) != 0:
		fr[0].decline()
		n = Notify.objects.get(pk=notify_id)
		n.notify_type = 'invite_partner_response_decline'
		new_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['invite_partner_response_decline'],
									{
										'username': user_add_request.username,
										'first_name': user_add_request.first_name ,
										'last_name': user_add_request.last_name,
									})
		n.content = new_content
		n.save()
		return simplejson.dumps({
									'notify_id': notify_id,
									'new_content': new_content,  
									'username':username,
									'firstname': user_add_request.first_name,
									'lastname': user_add_request.last_name,
									'reload':'False'
								})
	else:
		return simplejson.dumps({'reload':'True'})