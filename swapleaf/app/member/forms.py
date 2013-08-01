from django import forms
from django.contrib.auth.models import User
from django.utils import html
from django.utils.translation import ugettext_lazy as _, ugettext

from allauth.account import app_settings
from allauth.utils import email_address_exists

# Not done yet - Need to test and modify more
class SettingForm(forms.Form):
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
	zip_code = forms.CharField(max_length=5,required=False)

