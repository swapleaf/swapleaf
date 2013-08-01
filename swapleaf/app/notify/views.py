from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required

from swapleaf.app.main.utils import get_elapse_time
from swapleaf.app.main.models import Notify, Offer, BookTransaction
from swapleaf.helper.common import get_user_login_object, get_autocomplete_data, handle_request_get_message, get_new_notify

import datetime

@login_required()
def show_all_notification(request):
	now = datetime.datetime.now()
	message = handle_request_get_message(request)
	#autocomplete_data =  get_autocomplete_data(request)
	user_login = get_user_login_object(request)
	current_page = 1
	if 'page' in request.GET:
		current_page = int(request.GET['page'])
	all_notifies = Notify.objects.filter(notify_to=user_login).order_by("-date")
	last_page = int(len(all_notifies) / 10) + 1
	notifies = all_notifies[(current_page-1)*10:current_page*10] 
	for notify in notifies:
		elapse_time = now - notify.date
		notify.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		if notify.status == 'new': 
			notify.status = 'old'
		if notify.notify_type == "make_offer":
			offers = Offer.objects.filter(pk=notify.object_id)
			if len(offers) != 0:
				offer = offers[0]
				offer.view_status = "old"
				offer.save()
		notify.save()
	new_notify = get_new_notify(request)
	return render_to_response(
			"app/notify/page/main_view.html",
			{
				#"autocomplete_data": autocomplete_data,
				'message': message,
				"user_login": user_login,
				'current_page': current_page,
				'last_page': last_page,
				"notifies": notifies,
				'new_notify': new_notify
			},
			context_instance=RequestContext(request)
		)

@login_required()
def show_offer_notification(request):
	if request.method == "GET":
		now = datetime.datetime.now()
		transaction_id = request.GET['transaction_id']
		transactions = BookTransaction.objects.filter(transaction_id=transaction_id)
		user_login = get_user_login_object(request)
		message = handle_request_get_message(request)
		if len(transactions) == 0:
			return HttpResponseRedirect("/notification/error/")
		else:
			transaction = transactions[0]
			notifies = []
			if len(transaction.offer.all()) == 0:
				new_notify = get_new_notify(request)
				return render_to_response(
						"app/notify/page/offer_notification_not_found.html",
						{
							"user_login": user_login,
							'new_notify': new_notify,
						},
						context_instance=RequestContext(request)) 
			for offer in transaction.offer.all():
				offer.view_status = "old"
				offer.save()
				notify = Notify.objects.filter(notify_type='make_offer_price',object_id=offer.pk)
				print notify
				if len(notify) != 0:
					elapse_time = now - notify[0].date
					notify[0].elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
					if notify[0].status == 'new': 
						notify[0].status = 'old'
					notify[0].save()
					notifies.append(notify[0])
			notifies.sort(key=lambda r: r.date)
			new_notify = get_new_notify(request)
			return render_to_response(
				"app/notify/page/offer_notification.html",
				{
					#"autocomplete_data": autocomplete_data,
					'message': message,
					"user_login": user_login,
					"notifies": notifies,
					'new_notify': new_notify,
					'transaction': transaction
				},
				context_instance=RequestContext(request)
		)
	else:
		return HttpResponseRedirect("/notification/")

@login_required()
def notification_error(request):
	return HttpResponse("error")