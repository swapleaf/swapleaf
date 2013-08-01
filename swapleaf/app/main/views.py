from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.db import connection
#connection._rollback()

from swapleaf.helper.common import get_user_login_object, handle_request_get_message
from swapleaf.helper.common import get_new_notify, get_autocomplete_data
from swapleaf.app.main.models import BookTransaction, Offer

# Create your views here.
def main_view(request):
	message = handle_request_get_message(request)
	#autocomplete_data = get_autocomplete_data(request)
	new_notify = get_new_notify(request)
	#print autocomplete_data
	user_login = get_user_login_object(request)
	book_sell = BookTransaction.objects.filter(seller=user_login,transaction_type='1')
	all_book_sell = BookTransaction.objects.all()
	book_trade_give= BookTransaction.objects.filter(seller=user_login,transaction_type='2')
	#new_offer = Offer.objects.filter(user_receive=user_login,view_status='new')
	#all_offer = Offer.objects.filter(user_receive=user_login)
	#transaction_status = get_transaction_status(request)
	return render_to_response(
			"app/main/page/index.html",
			{
				'message': message,
				#'autocomplete_data': autocomplete_data,
				'new_notify': new_notify,
				'user_login': user_login,
				'book_sell': book_sell,
				'all_book_sell': all_book_sell,
				'book_trade_give': book_trade_give,
				#'new_offer': new_offer,
				#'all_offer': all_offer,
				#'transaction_status': transaction_status
			},
			context_instance=RequestContext(request)
		)