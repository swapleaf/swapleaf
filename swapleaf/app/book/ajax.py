from django.utils import simplejson
from django.template import RequestContext
from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register

from swapleaf.helper.common import get_user_login_object


@dajaxice_register
def handle_search_sell_book(request,course_number,price,condition,title,author,alert_email):
	request.session['book_condition'] = condition
	request.session['book_price'] = price
	request.session['book_title'] = title
	request.session['book_author'] = author
	request.session['course_number'] = course_number
	request.session['alert_email'] = alert_email
	return simplejson.dumps({})

@dajaxice_register
def handle_search_trade_give_book(request,course_number,condition,title,author,alert_email):
	request.session['book_condition'] = condition
	request.session['book_title'] = title
	request.session['book_author'] = author
	request.session['course_number'] = course_number
	request.session['alert_email'] = alert_email
	return simplejson.dumps({})

@dajaxice_register
def handle_search_title_author_buy_book(request,title,author,alert_email):
	request.session['title'] = title
	request.session['author'] = author
	request.session['alert_email'] = alert_email
	return simplejson.dumps({})

@dajaxice_register
def handle_course_buy_book(request,course_number,alert_email,school_id):
	request.session['course_number'] = course_number
	request.session['alert_email'] = alert_email
	request.session['school_id'] = school_id
	return simplejson.dumps({})

@dajaxice_register
def handle_search_isbn_buy_book(request,isbn,alert_email):
	request.session['alert_email'] = alert_email
	return simplejson.dumps({'isbn':isbn})

@dajaxice_register
def handle_search_available_book_author(request,author,alert_email):
	request.session['available_book_author'] = author
	request.session['alert_email'] = alert_email
	return simplejson.dumps({})