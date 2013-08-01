from django import forms
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _, ugettext


from swapleaf.helper.common import get_user_login_object, handle_request_get_message
from swapleaf.helper.common import get_autocomplete_data, get_new_notify
from swapleaf.helper.member import validate_email_setting
from swapleaf.helper.member import check_user_login_page, check_partnership
from swapleaf.app.main.models import BookTransaction, Institution
from swapleaf.app.member.forms import SettingForm


def main_view(request,username):
	user_view = get_object_or_404(User,username=username)
	user_login = get_user_login_object(request)
	
	#autocomplete_data = get_autocomplete_data(request)
	new_notify = get_new_notify(request)
	message = handle_request_get_message(request)

	template_name = ""
	if check_user_login_page(request,username):
		template = "app/member/page/view/login_user.html"
		is_partner = None
	else:
		template = "app/member/page/view/normal_user.html"
		is_partner = check_partnership(request,username)

	#book_trade_give = BookTradingGiving.objects.filter(trader1_giver=user_view)

	return render_to_response(
			template,
			{
				#'autocomplete_data': autocomplete_data,
				'message': message,
				'new_notify': new_notify,
				'is_partner': is_partner,
				'user_view': user_view,
				'user_login': user_login,
				#'book_trade_give': book_trade_give,
			},
			context_instance=RequestContext(request)
		)

@login_required()
def settings(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)

	# If there are parameter f in setting url, this mean the edit
	# setting process got some error, render a setting error template
	if "error" in request.GET:
		return render_to_response(
				"member_template/admin_page/settings_error.html",
				{
					"user_login": user_login,
				},
				context_instance=RequestContext(request)
			)
	if request.method == 'POST': 
		form = SettingForm(request.POST) 
		if form.is_valid(): 
			flag = True
			if validate_email_setting(request) == -1:
				form._errors["email"] = ErrorList([u"A user is registered with this e-mail address."])
				flag = False
			if flag:
				#try:
					# Save the new data to the object user and member (model Member)
				user_login.first_name = request.POST['first_name']
				user_login.last_name = request.POST['last_name']
				user_login.email = request.POST['email']
				if "institution" in request.POST and request.POST['institution'] != "None":
					institution_id = request.POST['institution']
					institution = Institution.objects.get(pk=institution_id)
					user_login.get_profile().school.student.remove(user_login)
					for course in user_login.get_profile().course.all():
						if course.institution == user_login.get_profile().school:
							user_login.get_profile().course.remove(course)
					user_login.get_profile().school = institution
					institution.student.add(user_login)
					institution.save()
				if 'zip_code' in request.POST and len(request.POST['zip_code']) != 0:
					user_login.get_profile().zip_code = int(request.POST['zip_code'])	
				user_login.save()
				user_login.get_profile().save()	
				#except:
					# give the parameter error in the url link so the website
					# render the error in setting page
				#	return HttpResponseRedirect("/settings/?error")
				# redirect to user main page if the edit process is successful
				return HttpResponseRedirect("/")
	else:
		# The initial data of the form taken from the user database 
		default_data = {
		       	"first_name": user_login.first_name,
				"last_name": user_login.last_name,
		       	"email": user_login.email,
		       	'zip_code': user_login.get_profile().zip_code,
		   	}
		form = SettingForm(default_data) 
	return render_to_response(
		"app/member/page/settings.html",
		{
			"form":form,
			"user_login":user_login,
			'new_notify': new_notify,
		},
		context_instance=RequestContext(request)
	)

