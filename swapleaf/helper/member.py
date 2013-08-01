from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import get_object_or_404

from swapleaf.app.app_settings import SESSION_KEY
from swapleaf.app.friends.models import Friendship, FriendshipRequest
from swapleaf.helper.common import get_user_login_object

from allauth.account import app_settings
from allauth.utils import email_address_exists


def check_user_login_page(request,username):
	if SESSION_KEY in request.session:
		user_id = request.session[SESSION_KEY]
		user_login = User.objects.get(pk=user_id)
		if user_login.username == username:
			return True
		else:
			return False
	else:
		return False

#  1: Partner
# -1: Not Partner
# -2: Waiting from invite request
#  2: Response to the invite request
def check_partnership(request,username):
	if SESSION_KEY in request.session:
		user1 = User.objects.get(pk=request.session[SESSION_KEY])
		user2 = get_object_or_404(User, username=username)
		fr1 = FriendshipRequest.objects.filter(from_user=user1,to_user=user2,accepted=False)
		if len(fr1) == 0:
			fr2 = FriendshipRequest.objects.filter(from_user=user2,to_user=user1,accepted=False)
			if len(fr2) == 0:
				fs = Friendship.objects.are_friends(user1,user2)
				if fs: 
					return 1
				else: 
					return -1
			else:
				return 2
		else:
			return -2
	else:
		return -1


def validate_email_setting(request):
	value = request.POST['email']
	user_login = get_user_login_object(request)
	email = user_login.email
	print email
	if value != email:
		if value and email_address_exists(value):
			return -1
		else:
			return 1
	else:
		return 1