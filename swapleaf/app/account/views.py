from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response

from swapleaf.helper.common import get_user_login_object
from swapleaf.app.account.models import SwapLeafEmailConfirmation, SwapLeafEmailAddress

from allauth.account.views import login as allauth_login
from allauth.account.views import signup as allauth_signup

# Create your views here.
def confirmation(request,confirmation_key):
    e = SwapLeafEmailConfirmation.objects.filter(confirmation_key=confirmation_key)
    if len(e) == 0:
      return HttpResponseRedirect("/?action=confirm_email&result=error")
    else:     
      try:
        email = e[0].email_address
        emailAddress = SwapLeafEmailAddress.objects.get(email=email)
        emailAddress.verified = True
        emailAddress.save()    	
        return HttpResponseRedirect("/?action=confirm_email&result=success")
      except:
        return HttpResponseRedirect("/?action=confirm_email&result=error")

def signup(request,**kwargs):
    user_login = get_user_login_object(request)
    if user_login:
        return HttpResponseRedirect("/")
    else:
        return allauth_signup(request,**kwargs)

def login(request,**kwargs):
    user_login = get_user_login_object(request)
    if user_login:
        return HttpResponseRedirect("/")
    else:
        return allauth_login(request,**kwargs)