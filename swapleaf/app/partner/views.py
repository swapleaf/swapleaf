from django import forms
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _, ugettext

from swapleaf.helper.common import get_user_login_object, handle_request_get_message
from swapleaf.helper.common import get_autocomplete_data, get_new_notify, remove_duplicate_object
from swapleaf.helper.member import validate_email_setting
from swapleaf.helper.member import check_user_login_page, check_partnership
from swapleaf.helper.account import get_people_by_name
from swapleaf.helper.partner import get_partners_data, get_partner_match_value
from swapleaf.app.main.models import BookTransaction, Institution
from swapleaf.app.member.forms import SettingForm


@login_required()
def main_view(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	people = []
	partners_data = get_partners_data(request)
	is_search = False
	if request.method == "GET":
		if "q" in request.GET:
			is_search = True
			query = request.GET['q']
			if len(query) != 0:
				people = get_people_by_name(request,query)
				for person in people:
					person.get_profile().partner_status = check_partnership(request,person.username)
					person.get_profile().save()
	return render_to_response(
			"app/partner/page/main_view.html",
			{
				'user_login': user_login,
				'people': people,
				'new_notify': new_notify,
				'is_search': is_search,
				'partners_data':partners_data
			},
			context_instance=RequestContext(request)
		)

@login_required()
def partner_book_available(request,username):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	partner = get_object_or_404(User,username=username)
	book_sell_trade = BookTransaction.objects.filter(seller=partner)
	if 'sort' in request.GET:
		if request.GET['sort'] == 'condition':
			book_sell_trade = BookTransaction.objects.filter(seller=partner).order_by('condition')
		elif request.GET['sort'] == 'post_time':
			book_sell_trade = BookTransaction.objects.filter(seller=partner).order_by('-post_time')
		elif request.GET['sort'] == 'title':
			list_book_sell_trade = BookTransaction.objects.filter(seller=partner)
			list_title = {}
			for book_sell_trade in list_book_sell_trade:
				list_title[book_sell_trade] = book_sell_trade.book.title
			book_sell_trade = sorted(list_title, key=list_title.get)
		else:
			list_book_sell_trade = BookTransaction.objects.filter(seller=partner)
			list_author = {}
			for book_sell_trade in list_book_sell_trade:
				list_author[book_sell_trade] = book_sell_trade.book.author
			book_sell_trade = sorted(list_author, key=list_author.get)
	return render_to_response(
							"app/partner/page/partner_book_available.html",
							{
								'user_login': user_login,
								'new_notify': new_notify,
								'partner': partner,
								'book_sell_trade': book_sell_trade
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def partner_book_wanted(request,username):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	partner = get_object_or_404(User,username=username)
	return render_to_response(
							"app/partner/page/partner_book_wanted.html",
							{
								'user_login': user_login,
								'new_notify': new_notify,
								'partner': partner,
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def partner_book_match(request,username):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	partner = get_object_or_404(User,username=username)
	user_login_transaction_book = BookTransaction.objects.filter(seller=user_login)
	partner_transaction_book = BookTransaction.objects.filter(seller=partner)

	books_sell_trade = []
	books_buy = []

	# Get all the book the user_login want to buy and the partner want to sell/trade
	for book_transaction in partner_transaction_book:
		for book_buying in user_login.get_profile().buy_book.all():
			if book_transaction.book == book_buying.book: 
				books_sell_trade.append(book_transaction)

	# Get all the book the user_login want to sell/trade and the partner want to buy
	for book_transaction in user_login_transaction_book:
		for book_buying in partner.get_profile().buy_book.all():
			if book_transaction.book == book_buying.book: 
				books_buy.append(book_transaction) 

	return render_to_response(
							"app/partner/page/partner_match.html",
							{
								'user_login': user_login,
								'new_notify': new_notify,
								'partner': partner,
								"books_buy": remove_duplicate_object(books_buy),
								'books_sell_trade': remove_duplicate_object(books_sell_trade)
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def partner_of_partner_match(request,username):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	partner = get_object_or_404(User,username=username)

	partner_match_data = []

	partners = user_login.get_profile().partners.all()
	for user1 in partners:
		for user2 in partners:
			if user1 != user2:
				partner_match_data += get_partner_match_value(user1,user2)

	return render_to_response(
							"app/partner/page/partner_of_partner_match.html",
							{
								'user_login': user_login,
								'new_notify': new_notify,
								'partner': partner,
								'partner_match_data': remove_duplicate_object(partner_match_data)
							}
							,context_instance=RequestContext(request)
						)

	