from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from swapleaf.helper.common import get_user_login_object, handle_request_get_message, convert_queryset_to_list
from swapleaf.helper.common import get_autocomplete_data, get_new_notify, remove_duplicate_object
from swapleaf.helper.account import check_confirm_user
from swapleaf.helper.book import search_book, get_book_by_title, get_book_by_author
from swapleaf.helper.book import get_book_by_title_and_author, get_book_by_course, get_book_by_isbn
from swapleaf.app.main.models import Book, BookTransaction, Course, Message, Notify, Offer, Institution, BookBuying
from swapleaf.app.app_settings import NOTIFY_SNIPPET_TEMPLATE
from swapleaf.settings import WEBSITE_HOMEPAGE
from swapleaf.app.main.utils import get_elapse_time

import datetime

@login_required()
def offer_time_location_form(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		try:
 			transaction_id = request.GET['transaction_id']
 			offer_id = request.GET['offer_id']
 			notify_id = request.GET['notify_id']
			transaction = BookTransaction.objects.get(transaction_id=transaction_id)
			offer = Offer.objects.get(pk=offer_id)
			notify = Notify.objects.get(pk=notify_id)
			return render_to_response(
						"app/offer/page/offer_form_time_location.html",
						{
							"user_login": user_login,
							"new_notify": new_notify,
							"transaction": transaction,
							'offer': offer,
							'notify': notify,
						}
						,context_instance=RequestContext(request)
					)	
		except:
			return HttpResponseRedirect('/offer/error/')	

@login_required()
def offer_time_location_process(request):
	if request.method == 'POST':
		#try:
		user_login = get_user_login_object(request)
		#offer_price = request.POST['offer_price_input']
		offer_message = request.POST['offer_message_textbox']
		
		offer_location = request.POST['offer_location_input']
		offer_year = int(request.POST['offer_date_input'][6:])
		offer_month = int(request.POST['offer_date_input'][0:2])
		offer_day = int(request.POST['offer_date_input'][3:5])
		print offer_year
		print offer_month
		print offer_day
		offer_hour = int(request.POST['offer_hour_input'])
		offer_minute = int(request.POST['offer_minute_input'])
		transaction_time = datetime.datetime(offer_year,offer_month,offer_day,offer_hour,offer_minute)
		
		#print offer_message
		transaction_id = request.POST['transaction_id']
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)	
		offer_id = request.POST['offer_id']
		notify_id = request.POST['notify_id']
		user_receive = Notify.objects.get(pk=notify_id).notify_from
		old_notify = Notify.objects.get(pk=notify_id)
		# if old_notify.notify_type == "make_offer_price":
		# 	other_notify = Notify.objects.get(notify_type='accept_offer_price',notify_from=old_notify.notify_to,notify_to=old_notify.notify_from)
		# 	pos = other_notify.content.find("<div class='time-location-area'>")
		# 	other_notify.content = other_notify.content[0:pos]
		# 	other_notify.save()
		# if old_notify.notify_type == "accept_offer_price":
		# 	other_notify = Notify.objects.get(notify_type='make_offer_price',notify_from=old_notify.notify_to,notify_to=old_notify.notify_from)
		# 	pos = other_notify.content.find("<div class='time-location-area'>")
		# 	other_notify.content = other_notify.content[0:pos]
		# 	other_notify.save()
		pos = old_notify.content.find("<div class='time-location-area'>")
		old_notify.content = old_notify.content[0:pos]
		old_notify.save()
		if transaction.status != "Pending":
			return HttpResponseRedirect("/")
		offer = Offer.objects.get(pk=offer_id)
		if len(offer_message) != 0:
			message = Message.objects.create(sender=user_login,receiver=transaction.seller,content=offer_message)
			offer.messages.add(message)	
			offer.last_message = message
		offer.transaction_time = transaction_time
		offer.location = offer_location
		#offer.view_status = "new"
		offer.save()
		if transaction.alert_email:
			subject = "You got suggestion for time and location of the book " + transaction.book.title
        	link = WEBSITE_HOMEPAGE + 'notification/offer/?transaction_id=' + transaction_id 
        	context = {
        		"link": link,
        		'name': user_login.first_name + ' ' + user_login.last_name,
        		'book_title': transaction.book.title
        	}
        	html_content = render_to_string('text/email/offer/suggest_time_location.html',context)
        	text_content = strip_tags(html_content)
        	mail = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [transaction.seller.email])
        	mail.attach_alternative(html_content, "text/html")
        	mail.send()
		notify = None
		notifies = Notify.objects.filter(notify_type='make_offer_time_location',notify_to=user_receive,notify_from=user_login,object_id=offer.pk)
		if len(notifies) == 0:
			notify = Notify.objects.create(notify_to=user_receive,notify_from=user_login,content='',notify_type='make_offer_time_location')
		else:
			notify = notifies[0]
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['make_offer_time_location'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'notify':  notify,
									'message': offer_message,
									'transaction': transaction,
									'offer': offer,
									'time': transaction_time,
									'location': offer_location,
								})
		notify.content = content
		notify.object_id = offer.pk 
		now = datetime.datetime.now()
		elapse_time = now - notify.date
		notify.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		notify.status = "new"
		notify.save()
		return HttpResponseRedirect("/")
		#return HttpResponseRedirect("/offer/time_location/success/")
		#except:
		#	return HttpResponseRedirect("/book/offer/error/")
	else:
		return HttpResponseRedirect('/')

@login_required()
def offer_price_form(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	# Clear session
	if "alert_email" in request.session:
		del request.session['alert_email']
	if "title" in request.session:
		del request.session['title']
	if "author" in request.session:
		del request.session['author']
	if "school_id" in request.session:
		del request.session['school_id']
	if "course_number" in request.session:
		del request.session['course_number']
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		try:
 			transaction_id = request.GET['transaction_id']
			transaction = BookTransaction.objects.get(transaction_id=transaction_id)
			return render_to_response(
						"app/offer/page/offer_form_price.html",
						{
							"user_login": user_login,
							"new_notify": new_notify,
							"transaction": transaction,
						}
						,context_instance=RequestContext(request)
					)	
		except:
			return HttpResponseRedirect('/offer/error/')	

@login_required()
def offer_price_process(request):
	if request.method == 'POST':
		#try:
		user_login = get_user_login_object(request)
		offer_price = request.POST['offer_price_input']
		offer_message = request.POST['offer_message_textbox']
		
		# offer_location = request.POST['offer_location_input']
		# offer_year = int(request.POST['offer_year_input'])
		# offer_month = int(request.POST['offer_month_input'])
		# offer_day = int(request.POST['offer_day_input'])
		# offer_hour = int(request.POST['offer_hour_input'])
		# offer_minute = int(request.POST['offer_minute_input'])
		# transaction_time = datetime.datetime(offer_year,offer_month,offer_day,offer_hour,offer_minute)
		
		#print offer_message
		transaction_id = request.POST['transaction_id']
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)	
		offers = Offer.objects.filter(user_offer=user_login,user_receive=transaction.seller)
		offer = None
		if len(offers) == 0:
			offer = Offer.objects.create(user_offer=user_login,user_receive=transaction.seller,price=offer_price)
		else:
			offer = offers[0]
		if len(offer_message) != 0:
			message = Message.objects.create(sender=user_login,receiver=transaction.seller,content=offer_message)
			offer.messages.add(message)	
			offer.last_message = message
		# offer.transaction_time = transaction_time
		# offer.location = offer_location
		offer.price = offer_price
		offer.offer_type = "1"
		offer.view_status = "new"
		offer.save()
		transaction.offer.add(offer)
		if transaction.alert_email:
			subject = "There is an offer for your copy of " + transaction.book.title
        	link = WEBSITE_HOMEPAGE + 'notification/offer/?transaction_id=' + transaction_id
        	context = {
        		"link": link,
        		'name': user_login.first_name + ' ' + user_login.last_name
        	}
        	html_content = render_to_string('text/email/offer/make_offer_price.html',context)
        	text_content = strip_tags(html_content)
        	mail = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [transaction.seller.email])
        	mail.attach_alternative(html_content, "text/html")
        	mail.send()
		notify = None
		notifies = Notify.objects.filter(notify_type='make_offer_price',notify_to=transaction.seller,notify_from=user_login,object_id=offer.pk)
		if len(notifies) == 0:
			notify = Notify.objects.create(notify_to=transaction.seller,notify_from=user_login,content='',notify_type='make_offer_price')
		else:
			notify = notifies[0]
		normal_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['make_offer_price_normal_content'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'notify':  notify,
									'price': offer_price,
									'message': offer_message,
									'transaction': transaction,
									'offer': offer,
									# 'time': transaction_time,
									# 'location': offer_location,
								})
		offer_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['make_offer_price_offer_content'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'notify':  notify,
									'price': offer_price,
									'message': offer_message,
									'transaction': transaction,
									'offer': offer,
									# 'time': transaction_time,
									# 'location': offer_location,
								})
		notify.content = normal_content
		notify.offer_content = offer_content
		notify.object_id = offer.pk 
		now = datetime.datetime.now()
		elapse_time = now - notify.date
		notify.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		notify.status = "new"
		notify.save()
		return HttpResponseRedirect("/")
		#return HttpResponseRedirect("/offer/price/success/")
		#except:
		#	return HttpResponseRedirect("/book/offer/error/")
	else:
		return HttpResponseRedirect('/')

@login_required()
def offer_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/offer/page/offer_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def offer_price_success(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/offer/page/offer_price_success.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def offer_time_location_success(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/offer/page/offer_time_location_success.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def counter_offer_price_form(request,offer_id):	
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/notification/")
	else:
		#try:
		user_login = get_user_login_object(request)
		new_notify = get_new_notify(request)
		offer = Offer.objects.get(pk=offer_id)
		transaction_id = request.GET['transaction_id']
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		return render_to_response(
					"app/offer/page/counter_offer_form_price.html",
					{
						"user_login": user_login,
						"new_notify": new_notify,
						'offer': offer,
						"transaction": transaction,
					}
					,context_instance=RequestContext(request)
				)
		#except:
		#	return HttpResponseRedirect("/notification/error")

@login_required()
def counter_offer_price_check(request):
	if "max_offer_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		user_login = get_user_login_object(request)
		new_notify = get_new_notify(request)
		max_offer_id = request.GET['max_offer_id']
		max_offer = Offer.objects.get(pk=max_offer_id)
		counter_price = request.session['counter_price']
		message = request.session['message']
		transaction_id = request.session['transaction_id'] 
		offer_id = request.session['offer_id'] 
		user_receive = Offer.objects.get(pk=offer_id).user_offer
		return render_to_response(
					"app/offer/page/counter_offer_price_check.html",
					{
						'user_login': user_login,
						'new_notify': new_notify,
						'max_offer': max_offer,
						'offer_id': offer_id,
						'message': message,
						'transaction_id': transaction_id,
						'counter_price': counter_price,
						'user_receive': user_receive
					}
					,context_instance=RequestContext(request)
				)

@login_required()
def counter_offer_price_process(request):
	if request.method == 'POST':
		#try:
		user_login = get_user_login_object(request)

		# Get offer data from the form
		offer_id = int(request.POST['offer_id'])
		offer_price = request.POST['offer_price_input']
		offer_message = request.POST['offer_message_textbox']

		offer = Offer.objects.get(pk=offer_id)
		# offer_location = request.POST['offer_location_input']
		# offer_year = int(request.POST['offer_year_input'])
		# offer_month = int(request.POST['offer_month_input'])
		# offer_day = int(request.POST['offer_day_input'])
		# offer_hour = int(request.POST['offer_hour_input'])
		# offer_minute = int(request.POST['offer_minute_input'])
		# transaction_time = datetime.datetime(offer_year,offer_month,offer_day,offer_hour,offer_minute)

		# Get transaction data from the form
		transaction_id = request.POST['transaction_id']
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		transaction.price = offer_price

		if request.POST['check_price'] == "True":
			check = False
			max_bid = transaction.offer.all()[0].price
			max_offer_id = transaction.offer.all()[0].pk
			for o in transaction.offer.all():
				if offer.offer_type == "1":
					if float(o.price) > float(offer_price):
						check = True
					if float(o.price) > float(max_bid):
						max_bid = o.price
						max_offer_id = o.pk
			if check:
				request.session['counter_price'] = offer_price
				request.session['offer_id'] = offer_id
				request.session['message'] = offer_message
				request.session['transaction_id'] = transaction_id
				return HttpResponseRedirect("/offer/counter/price/check/?max_offer_id=" + str(max_offer_id))
		

		user_receive = Offer.objects.get(pk=offer_id).user_offer
		counter_offers = Offer.objects.filter(user_offer=user_login,user_receive=user_receive)
		counter_offer = None
		if len(counter_offers) == 0:
			counter_offer = Offer.objects.create(user_offer=user_login,user_receive=user_receive,price=offer_price)
		else:
			counter_offer = counter_offers[0]
		if len(offer_message) != 0:
			message = Message.objects.create(sender=user_login,receiver=user_receive,content=offer_message)
			counter_offer.messages.add(message)	
			counter_offer.last_message = message
		# counter_offer.transaction_time = transaction_time
		# counter_offer.location = offer_location
		counter_offer.price = offer_price
		counter_offer.offer_type = "2"
		counter_offer.view_status = "new"
		counter_offer.save()
		transaction.offer.add(counter_offer)
		transaction.save()
		#if transaction.alert_email:
		subject = "You got a counter offer for your copy of " + transaction.book.title
		link = WEBSITE_HOMEPAGE + 'notification/offer/?transaction_id=' + str(transaction.transaction_id)
		context = {
        		"link": link,
        		'name': user_login.first_name + ' ' + user_login.last_name
			}
		html_content = render_to_string('text/email/offer/make_counter_offer_price.html',context)
		text_content = strip_tags(html_content)
		mail = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_receive.email])
		mail.attach_alternative(html_content, "text/html")
		mail.send()
		notify = None
		notifies = Notify.objects.filter(notify_type='make_counter_offer_price',notify_to=user_receive,notify_from=user_login,object_id=counter_offer.pk)
		if len(notifies) == 0:
			notify = Notify.objects.create(notify_type='make_counter_offer_price',notify_to=user_receive,notify_from=user_login)
		else:
			notify = notifies[0]
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['make_counter_offer_price'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'notify_id':  notify.pk,
									'price': offer_price,
									'message': offer_message,
									'transaction': transaction,
									'offer_id': counter_offer.id,
									# 'time': transaction_time,
									# 'location': offer_location,
								})
		notify.content = content
		notify.object_id = counter_offer.pk 
		now = datetime.datetime.now()
		elapse_time = now - notify.date
		notify.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		notify.status = "new"
		notify.save()

		update_notifies = Notify.objects.filter(notify_type='make_offer_price',object_id=offer_id)
		if len(update_notifies) != 0:
			update_notify = update_notifies[0]
			normal_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['counter_offer_price_notice_normal_content'],
									{
									'username': user_receive.username,
									'first_name': user_receive.first_name,
									'last_name': user_receive.last_name,
									'counter_price': offer_price,
									#'counter_message': offer_message,
									'transaction': transaction,
									'notify': update_notify,
									'offer': offer,
									'now': now,
									# 'time': transaction_time,
									# 'location': offer_location,
								})
			offer_content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['counter_offer_price_notice_offer_content'],
								{
									'username': user_receive.username,
									'first_name': user_receive.first_name,
									'last_name': user_receive.last_name,
									'counter_price': offer_price,
									#'counter_message': offer_message,
									'transaction': transaction,
									'notify': update_notify,
									'offer': offer,
									'now': now,
									# 'time': transaction_time,
									# 'location': offer_location,
								})
			update_notify.content = normal_content 
			update_notify.offer_content = offer_content
			update_notify.save()
		return HttpResponseRedirect("/")
		#return HttpResponseRedirect("/offer/price/success/")
		#except:
		#	return HttpResponseRedirect("/book/offer/error/")
	else:
		return HttpResponseRedirect('/')

@login_required()
def accept_offer_price_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "offer_id" not in request.GET or "notify_id" not in request.GET or "transaction_id" not in request.GET:	
		return HttpResponseRedirect("/")
	else:
		#try:
		offer_id = request.GET['offer_id']
		notify_id = request.GET['notify_id']
		transaction_id = request.GET['transaction_id']
		offer = Offer.objects.get(pk=offer_id)
		notify = Notify.objects.get(pk=notify_id)
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		return render_to_response(
							"app/offer/page/accept_offer_price_confirm.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'offer': offer,
								'transaction': transaction,
								'notify': notify,
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def accept_offer_price_process(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "offer_id" not in request.GET or "notify_id" not in request.GET or "transaction_id" not in request.GET:	
		return HttpResponseRedirect("/")
	else:
		#try:
		offer_id = request.GET['offer_id']
		notify_id = request.GET['notify_id']
		transaction_id = request.GET['transaction_id']
		offer = Offer.objects.get(pk=offer_id)
		notify = Notify.objects.get(pk=notify_id)
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		transaction.status = 'Pending'
		transaction.price = offer.price
		#transaction.location = offer.location
		transaction.buyer = user_login
		#transaction.transaction_time = offer.transaction_time
		transaction.save()
		user_receive = None
		if notify.notify_to == user_login:
			user_receive = notify.notify_from
		else:
			user_receive = notify.notify_to
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['accept_offer_price_notice'],
									{
									'username': user_receive.username,
									'first_name': user_receive.first_name,
									'last_name': user_receive.last_name,
									'notify': notify,
									'offer': offer,
									'transaction': transaction
								})
		notify.content = content
		notify.save()
		n = Notify.objects.filter(notify_type='accept_offer_price',notify_to=offer.user_offer,notify_from=user_login)
		if len(n) == 0:
			ntf = Notify.objects.create(notify_type='accept_offer_price',notify_to=offer.user_offer,notify_from=user_login)
		else:
			ntf = n[0]
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['accept_offer_price'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'ntf': ntf,
									'offer': offer,
									'transaction': transaction
								})
		ntf.content = content
		now = datetime.datetime.now()
		elapse_time = now - ntf.date
		ntf.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		ntf.status = "new"
		ntf.save()
		return render_to_response(
							"app/offer/page/accept_offer_price_success.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'transaction': transaction,
								'offer': offer,
								'notify': notify,
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def accept_offer_time_location_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "offer_id" not in request.GET or "notify_id" not in request.GET or "transaction_id" not in request.GET:	
		return HttpResponseRedirect("/")
	else:
		#try:
		offer_id = request.GET['offer_id']
		notify_id = request.GET['notify_id']
		transaction_id = request.GET['transaction_id']
		offer = Offer.objects.get(pk=offer_id)
		notify = Notify.objects.get(pk=notify_id)
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		return render_to_response(
							"app/offer/page/accept_offer_time_location_confirm.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'offer': offer,
								'transaction': transaction,
								'notify': notify,
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def accept_offer_time_location_process(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "offer_id" not in request.GET or "notify_id" not in request.GET or "transaction_id" not in request.GET:	
		return HttpResponseRedirect("/")
	else:
		#try:
		offer_id = request.GET['offer_id']
		notify_id = request.GET['notify_id']
		transaction_id = request.GET['transaction_id']
		offer = Offer.objects.get(pk=offer_id)
		notify = Notify.objects.get(pk=notify_id)
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		transaction.status = 'Complete'
		transaction.location = offer.location
		transaction.buyer = user_login
		transaction.transaction_time = offer.transaction_time
		transaction.save()
		user_receive = None
		if notify.notify_to == user_login:
			user_receive = notify.notify_from
		else:
			user_receive = notify.notify_to
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['accept_offer_time_location_notice'],
									{
									'username': user_receive.username,
									'first_name': user_receive.first_name,
									'last_name': user_receive.last_name,
									'notify': notify,
									'offer': offer,
									'transaction': transaction,
									'time': transaction.transaction_time,
									'location': transaction.location
								})
		notify.content = content
		notify.save()
		n = Notify.objects.filter(notify_type='accept_offer_time_location',notify_to=offer.user_offer,notify_from=user_login)
		if len(n) == 0:
			ntf = Notify.objects.create(notify_type='accept_offer_time_location',notify_to=offer.user_offer,notify_from=user_login)
		else:
			ntf = n[0]
		content = render_to_string(NOTIFY_SNIPPET_TEMPLATE['accept_offer_time_location'],
									{
									'username': user_login.username,
									'first_name': user_login.first_name,
									'last_name': user_login.last_name,
									'ntf': ntf,
									'offer': offer,
									'transaction': transaction
								})
		ntf.content = content
		now = datetime.datetime.now()
		elapse_time = now - ntf.date
		ntf.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		ntf.status = "new"
		ntf.save()
		return render_to_response(
							"app/offer/page/accept_offer_time_location_success.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'transaction': transaction,
								'offer': offer,
								'notify': notify,
							}
							,context_instance=RequestContext(request)
						)


@login_required()
def decline_offer(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if "offer_id" not in request.GET or "notify_id" not in request.GET or "transaction_id" not in request.GET:	
		return HttpResponseRedirect("/")
	else:
		#try:
		offer_id = request.GET['offer_id']
		notify_id = request.GET['notify_id']
		transaction_id = request.GET['transaction_id']
		offer = Offer.objects.get(pk=offer_id)
		notify = Notify.objects.get(pk=notify_id)
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		return render_to_response(
							"app/offer/page/decline_offer.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'offer': offer,
							}
							,context_instance=RequestContext(request)
						)
