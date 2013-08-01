#import re

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import get_object_or_404

from swapleaf.helper.common import get_user_login_object, convert_queryset_to_list, remove_duplicate_object
from swapleaf.app.account.models import SwapLeafEmailAddress, SwapLeafEmailConfirmation
from swapleaf.app.app_settings import IGNORE_WORDS

#alnum_re = re.compile(r"^\w+$")

# Helper for member app. Input: dtn1712@gmail.com -> Output: dtn1712
def get_prefix_email(email):
	result = ""
	for i in range(0,len(email)):
		if email[i] == "@":
			break
		result = result + email[i]
	return result.replace('.','_')

# Set a readable username created from analyze the first name, last name
# and email. Use this when create new member since it is just required
# user to enter email for registration, not username
def set_readable_username(email):
	name = get_prefix_email(email)
	u = User.objects.filter(username=name)
	if len(u) == 0:
		return name
	else:
		i = 1
		while len(u) != 0:
			test_username = name + str(i)
			u = User.objects.filter(username=test_username)
			if len(u) == 0: 
				return test_username
			i = i + 1

# Return value:
#	_ -2: user login, but no email confirmation sent
#	_ -1: user not login
#	_  0: user login and not confirm
#	_  1: user login and confirmed
def check_confirm_user(request):
	user_login = get_user_login_object(request)
	if user_login:
		email_confirmation = SwapLeafEmailAddress.objects.filter(email=user_login.email)
		if len(email_confirmation) != 0:
			if email_confirmation[0].verified == False: 
				return 0
			else:
				return 1
		else:
			return -2
	return -1

def get_people_by_name(request,query):
	user_login = get_user_login_object(request)
	author_words = query.split()
	result = []
	for word in author_words:
		if word.lower() not in IGNORE_WORDS:
			users1 = convert_queryset_to_list(User.objects.filter(first_name__icontains=word).exclude(pk=1).exclude(pk=user_login.pk))
			users2 = convert_queryset_to_list(User.objects.filter(last_name__icontains=word).exclude(pk=1).exclude(pk=user_login.pk))
			users = users1 + users2
			result = result + users
	return remove_duplicate_object(result)

def resend_email_confirmation(user):
	e = SwapLeafEmailConfirmation.objects.filter(email_address=user.email)
	if len(e) != 0:
		email_confirm = e[0]    
		email_confirm.send_confirmation()        
	else:
		new_email_confirm = SwapLeafEmailConfirmation.objects.create(email_address=user.email,sent=datetime.datetime.now())
		new_email_address = SwapLeafEmailAddress.objects.create(user=user,email=user.email)
		new_email_confirm.save()
		new_email_address.save()
		new_email_confirm.send_confirmation()