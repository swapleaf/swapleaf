from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import get_object_or_404

from swapleaf.app.friends.models import Friendship, FriendshipRequest
from swapleaf.helper.common import get_user_login_object, convert_queryset_to_list, remove_duplicate_object
from swapleaf.helper.member import check_partnership
from swapleaf.app.main.models import BookTransaction

from allauth.account import app_settings
from allauth.utils import email_address_exists


def get_partner_match_number(user1,user2):
	list_buy_book1 = user1.get_profile().buy_book.all()
	list_buy_book2 = user2.get_profile().buy_book.all()
	list_transaction_book1 = BookTransaction.objects.filter(seller=user1)
	list_transaction_book2 = BookTransaction.objects.filter(seller=user2)
	matches = 0
	for book_transaction in list_transaction_book1:
		for book_buying in list_buy_book2:
				if book_transaction.book == book_buying.book: 
					matches += 1

	for book_transaction in list_transaction_book2:
		for book_buying in list_buy_book1:
				if book_transaction.book == book_buying.book: 
					matches += 1		
	return matches	


def get_partner_match_value(user1,user2):
	list_buy_book1 = user1.get_profile().buy_book.all()
	list_buy_book2 = user2.get_profile().buy_book.all()
	list_transaction_book1 = BookTransaction.objects.filter(seller=user1)
	list_transaction_book2 = BookTransaction.objects.filter(seller=user2)
	result = []
	for book_transaction in list_transaction_book1:
		for book_buying in list_buy_book2:
				if book_transaction.book == book_buying.book: 
					result.append((book_transaction,user1,user2))

	for book_transaction in list_transaction_book2:
		for book_buying in list_buy_book1:
				if book_transaction.book == book_buying.book: 
					result.append((book_transaction,user2,user1))		
	return result


def get_partners_data(request):
	user_login = get_user_login_object(request)
	list_buy_book = convert_queryset_to_list(user_login.get_profile().buy_book.all())
	list_transaction_book = BookTransaction.objects.filter(seller=user_login)
	result = []
	#users = User.objects.all()
	partners = user_login.get_profile().partners.all()
	for user in partners:
		#if check_partnership(request,user.username) == 1 and user != user_login:
		book_transactions1 = BookTransaction.objects.filter(seller=user)
		matches = 0
		partner_match = 0

		# Get all the book the user_login want to buy and the partner want to sell/trade
		for book_transaction in book_transactions1:
			for book_buying in list_buy_book:
				if book_transaction.book == book_buying.book: 
					matches += 1

		# Get all the book the user_login want to sell/trade and the partner want to buy
		for book_transaction in list_transaction_book:
			for book_buying in user.get_profile().buy_book.all():
				if book_transaction.book == book_buying.book: 
					matches += 1 

		for user2 in partners:
			if user2 != user:
				partner_match += get_partner_match_number(user2,user)

		# Get the match for partners of the user_login's partners
		# for partner in user.get_profile().partners.all():
		# 	if partner != user_login:
		# 		book_transactions2 = BookTransaction.objects.filter(seller=partner)
		# 		m1 = 0
		# 		for book_transaction in book_transactions2:
		# 			for book_buying in list_buy_book:
		# 				if book_transaction.book == book_buying.book: 
		# 					m1 += 1
		# 		partner_match += m1
		# 		m2 = 0
		# 		for book_transaction in list_transaction_book:
		# 			for book_buying in partner.get_profile().buy_book.all():
		# 				if book_transaction.book == book_buying.book:
		# 					m2 += 1
		# 		partner_match += m2
		result.append([user,len(book_transactions1),matches,partner_match])
	return result