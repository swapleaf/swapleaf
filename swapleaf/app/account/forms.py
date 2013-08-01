import base64
import re
import uuid
import datetime

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.http import int_to_base36
from django.utils.importlib import import_module

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404

from swapleaf.helper.account import set_readable_username
from swapleaf.app.main.models import USA_STATES, Institution
        
from allauth.account import app_settings
from allauth.utils import email_address_exists

from swapleaf.app.account.models import SwapLeafEmailConfirmation, SwapLeafEmailAddress

class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', 
                                  app_settings.PASSWORD_INPUT_RENDER_VALUE)
        kwargs['widget'] = forms.PasswordInput(render_value=render_value)
        super(PasswordField, self).__init__(*args, **kwargs)

class SetPasswordField(PasswordField):

    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if len(value) < min_length:
            raise forms.ValidationError(_("Password must be a minimum of {0} "
                                          "characters.").format(min_length))
        return value

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(
        label = _("Firstname"),
        max_length = 40,
        widget = forms.TextInput()
    )
    last_name = forms.CharField(
        label = _("Lastname"),
        max_length = 40,
        widget = forms.TextInput()
    )
    email = forms.EmailField(max_length=60,widget=forms.TextInput())
    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Confirm Password"))
    # state = forms.ChoiceField(choices=USA_STATES)
    zip_code = forms.CharField(max_length=5,required=False)
    
    def clean_email(self):
        value = self.cleaned_data["email"]
        if app_settings.UNIQUE_EMAIL:
            if value and email_address_exists(value):
                raise forms.ValidationError \
                    (_("A user is registered with this e-mail address."))
        return value

    def clean(self):
        super(CustomSignupForm, self).clean()
        if app_settings.SIGNUP_PASSWORD_VERIFICATION \
                and "password1" in self.cleaned_data \
                and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
    
    def create_user(self,request=None):
        email = self.cleaned_data['email']
        username = set_readable_username(email)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user = User.objects.create(username=username,email=email,first_name=first_name,last_name=last_name)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        zip_code = self.cleaned_data.get("zip_code")
        if zip_code:
            user.get_profile().zip_code = int(zip_code)
        try:
            if "institution" in request.POST and request.POST['institution'] != "None":
                institution_id = request.POST['institution']
                institution = Institution.objects.get(pk=institution_id)
                user.get_profile().school = institution
                institution.student.add(user_login)
                institution.save()
        except:
            pass
        user.save()
        user.get_profile().save()
        return user

    def send_activate_mail(self,user):
        email = user.email
        e = SwapLeafEmailConfirmation.objects.filter(email_address=email)
        is_sent = True
        if len(e) == 0:
            is_sent = False
        if is_sent:
            email_confirm = e[0]    
            email_confirm.send_confirmation()        
        else:
            new_email_confirm = SwapLeafEmailConfirmation.objects.create(email_address=email,sent=datetime.datetime.now())
            new_email_address = SwapLeafEmailAddress.objects.create(user=user,email=email)
            new_email_confirm.save()
            new_email_address.save()
            new_email_confirm.send_confirmation()

    def save(self,request=None):
        user = self.create_user(request)
        self.send_activate_mail(user)
        return user