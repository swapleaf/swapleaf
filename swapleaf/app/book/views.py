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
from swapleaf.helper.book import search_book, get_book_by_title, get_book_by_author, get_authors
from swapleaf.helper.book import get_book_by_title_and_author, get_book_by_course, get_book_by_isbn
from swapleaf.app.main.models import Book, BookTransaction, Course, Message, Notify, Offer, Institution, BookBuying, BookAvailableAuthor
from swapleaf.app.app_settings import NOTIFY_SNIPPET_TEMPLATE
from swapleaf.settings import WEBSITE_HOMEPAGE
from swapleaf.app.main.utils import get_elapse_time

import datetime
import uuid 

########################################
#                                      #
#               BUY BOOK               #
#                                      #
########################################
@login_required()
def buy_book_form(request):
	new_notify = get_new_notify(request)
	user_login = get_user_login_object(request)
	return render_to_response(
				"app/book/page/buy/buy_form.html",
				{
					'user_login': user_login,
					'new_notify': new_notify
				}
				,context_instance=RequestContext(request))

# Confirm screen for add course class
@login_required()
def buy_book_course_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	course_number = None
	school = None
	if "course_number" in request.session:
		course_number = request.session['course_number']
	if 'school_id' in request.session:
		school_id = request.session['school_id']
		school = Institution.objects.get(pk=school_id)
	return render_to_response(
	 			"app/book/page/buy/buy_book_course_confirm.html",
	 			{
	 				'user_login': user_login,
	 				'new_notify': new_notify,
	 				'course_number': course_number.upper(),
	 				'school': school,
	 			}
	 			,context_instance=RequestContext(request))


@login_required()
def buy_book_search_course_listed(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	course_number = None
	school = None
	if "course_number" in request.GET:
		course_number = request.GET['course_number']
	if 'school_id' in request.GET:
		school_id = request.GET['school_id']
	books =  get_book_by_course(request,course_number,school_id)
	if len(books) == 0:
		return HttpResponseRedirect("/book/buy/search/not_found")
	else:
		listed_books = []
		for book in books:
			listed = convert_queryset_to_list(BookTransaction.objects.filter(book=book).exclude(seller=user_login))
			listed_books = listed_books + listed
		return render_to_response(
				"app/book/page/buy/buy_book_listed.html",
				{
					'user_login': user_login,
					'new_notify': new_notify,
					'listed_books': remove_duplicate_object(listed_books)
				}
				,context_instance=RequestContext(request))


@login_required()
def buy_book_search_isbn_listed(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	book_isbn = None
	if "book_isbn" in request.GET:
		book_isbn = request.GET['book_isbn']
	books =  get_book_by_isbn(book_isbn)
	if len(books) == 0:
		return HttpResponseRedirect('/book/buy/search/not_found')
	else:
		listed_books = convert_queryset_to_list(BookTransaction.objects.filter(book=books[0]).exclude(seller=user_login))
		return render_to_response(
			"app/book/page/buy/buy_book_listed.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'listed_books': listed_books
			}
			,context_instance=RequestContext(request))


@login_required()
def buy_book_course_process(request):
	user_login = get_user_login_object(request)
	course_number = None
	school = None
	if 'school_id' in request.GET:
		school_id = request.session['school_id']
		school = Institution.objects.get(pk=school_id)
	if "course_number" in request.GET:
		course_number = request.GET['course_number']
		course = None
		courses = Course.objects.filter(institution=school,course_number=course_number)
		if len(courses)  == 0:
			course = Course.objects.create(institution=school,course_number=course_number)
		else:
			course = courses[0]
		user_login.get_profile().course.add(course)
		user_login.get_profile().save()
		user_login.save()
	return HttpResponseRedirect("/")


# Search book by using title and author
@login_required()
def buy_book_search_title_author(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	title,author = "",""
	if 'title' in request.session:
		title = request.session['title']
	if 'author' in request.session:
		author =  request.session['author']
	books =  []
	if len(title) != 0 and len(author) != 0:
		books = get_book_by_title_and_author(title,author)
	else:
		if len(title) != 0:
			books = get_book_by_title(title)
		elif len(author) != 0:
			books = get_book_by_author(author)
	#book_sellings = BookTransaction.objects.filter(transaction_type='1')
	return render_to_response(
			"app/book/page/buy/buy_search.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'books': books,
				#'book_sellings': book_sellings
			}
			,context_instance=RequestContext(request))


# Search the selling book by isbn -> go directly to the listed selling book
@login_required()
def buy_book_search_isbn(request,book_isbn):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	books =  get_book_by_isbn(book_isbn)
	if len(books) == 0:
		return HttpResponseRedirect('/book/buy/search/not_found')
	else:
		# print books
		# listed_books = convert_queryset_to_list(BookTransaction.objects.filter(book=books[0]).exclude(seller=user_login))
		# print listed_books
		# return render_to_response(
		# 	"app/book/page/buy/buy_book_listed.html",
		# 	{
		# 		'user_login': user_login,
		# 		'new_notify': new_notify,
		# 		'listed_books': listed_books
		# 	}
		# 	,context_instance=RequestContext(request))
		return render_to_response(
			"app/book/page/buy/buy_search.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'books': books,
				#'book_sellings': book_sellings
			}
			,context_instance=RequestContext(request))

@login_required()
def buy_book_add_item_process(request,book_isbn):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	try: 
		book = None
		if len(book_isbn) == 10:
			books = Book.objects.filter(isbn10=book_isbn)
			if len(books) != 0:
				book = books[0]
		elif len(book_isbn) == 13:
			books = Book.objects.filter(isbn13=book_isbn)
			if len(books) != 0:
				book = books[0]
		else:
			return HttpResponseRedirect("/book/buy/error")
		alert_email = True
		if 'alert_email' in request.session:
			if request.session['alert_email'] == "0":
				alert_email = False
		book_buying_list = BookBuying.objects.filter(book=book)
		book_buying = None
		if len(book_buying_list) == 0:
			book_buying = BookBuying.objects.create(book=book)
		else:
			book_buying = book_buying_list[0]
		book_buying.alert_email = alert_email
		book_buying.save()
		user_login.get_profile().buy_book.add(book_buying)
		user_login.get_profile().save()
		return HttpResponseRedirect("/")
	except Book.DoesNotExist:
		return HttpResponseRedirect("/book/buy/error")

# @login_required()
# def buy_book_available_author_listed(request):
# 	user_login = get_user_login_object(request)
# 	new_notify = get_new_notify(request)
# 	available_book_author = None
# 	if "available_book_author" in request.session:
# 		available_book_author = request.session['available_book_author']
# 	#authors = get_authors(available_book_author)
# 	return render_to_response(
# 	 			"app/book/page/buy/buy_book_available_author_confirm.html",
# 	 			{
# 	 				'user_login': user_login,
# 	 				'new_notify': new_notify,
# 	 				'authors': authors,
# 	 			}
# 	 			,context_instance=RequestContext(request))

@login_required()
def buy_book_available_author_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	available_book_author = ""
	if "available_book_author" in request.session:
		available_book_author = request.session['available_book_author']
	#authors = get_authors(available_book_author)
	lst = [word[0].upper() + word[1:] for word in available_book_author.split()]
	author = " ".join(lst)
	return render_to_response(
	 			"app/book/page/buy/buy_book_available_author_confirm.html",
	 			{
	 				'user_login': user_login,
	 				'new_notify': new_notify,
	 				'author':author
	 			}
	 			,context_instance=RequestContext(request))

@login_required()
def buy_book_available_author_process(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	available_book_author = ""
	if "available_book_author" in request.GET:
		available_book_author = request.GET['available_book_author']
	available_book_author = BookAvailableAuthor.objects.create(author=available_book_author)
	available_book_author.save()
	user_login.get_profile().available_book_author.add(available_book_author)
	return HttpResponseRedirect("/")

@login_required()
def delete_available_book_author(request):
	if "available_book_author_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		user_login = get_user_login_object(request)
		try:
			available_book_author_id = request.GET['available_book_author_id']
			for available_book_author in user_login.get_profile().available_book_author.all():
				if int(available_book_author.pk) == int(available_book_author_id):
					user_login.get_profile().available_book_author.remove(available_book_author)
			user_login.get_profile().save()
			return HttpResponseRedirect("/")
		except:
			return HttpResponseRedirect("/book/buy/author/available_book/delete/error")

@login_required()
def delete_available_book_author_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/delete_available_book_author_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def edit_buy_book_item(request):
	if "buy_book_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		user_login = get_user_login_object(request)
		new_notify = get_new_notify(request)
		try:
			buy_book_id = request.GET['buy_book_id']
			buy_book = BookBuying.objects.get(pk=buy_book_id)
			return render_to_response(
					"app/book/page/buy/buy_book_edit.html",
					{
						'user_login': user_login,
						'new_notify': new_notify,
						'buy_book': buy_book
					}
					,context_instance=RequestContext(request))
		except:
			return HttpResponseRedirect("/book/buy/item/edit/error")

@login_required()
def edit_buy_book_item_process(request):
	if 'alert_email' not in request.GET or "buy_book_id" not in request.GET:
		return HttpResponseRedirect("/book/buy/item/edit/error")
	else:
		try:
			buy_book_id = request.GET['buy_book_id']
			buy_book = BookBuying.objects.get(pk=buy_book_id)
			alert_email = request.GET['alert_email']
			
			if alert_email == '0':
				buy_book.alert_email = False
			else:
				buy_book.alert_email = True
			buy_book.save()
			return HttpResponseRedirect("/")
		except:
			return HttpResponseRedirect("/book/buy/item/edit/error")


@login_required()
def edit_buy_book_item_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/edit_buy_book_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def delete_buy_book_item(request):
	if "buy_book_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		user_login = get_user_login_object(request)
		try:
			buy_book_id = request.GET['buy_book_id']
			for buy_book in user_login.get_profile().buy_book.all():
				if int(buy_book.pk) == int(buy_book_id):
					user_login.get_profile().buy_book.remove(buy_book)
			user_login.get_profile().save()
			return HttpResponseRedirect("/")
		except:
			return HttpResponseRedirect("/book/buy/item/delete/error")

@login_required()
def delete_buy_book_item_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/delete_buy_book_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)



@login_required() 
def buy_book_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
			"app/book/page/buy/buy_search_error.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
			}
			,context_instance=RequestContext(request))


@login_required()
def buy_book_search_not_found(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
			"app/book/page/buy/buy_search_not_found.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
			}
			,context_instance=RequestContext(request))


########################################
#                                      #
#             SELL BOOK                #
#                                      #
########################################
@login_required()
def sell_book_form(request):
	new_notify = get_new_notify(request)
	user_login = get_user_login_object(request)
	if request.method == 'POST':
		isbn = request.POST['book_isbn_input']
		request.session['book_isbn'] = isbn
		request.session['book_condition'] = None
		request.session['book_price'] = None
		request.session['course_number'] = None
		request.session['alert_email'] = request.POST['alert_email_input']
		if "book_condition_input" in request.POST:
			request.session['book_condition'] = request.POST['book_condition_input']
		if "book_price_input" in request.POST:
			request.session['book_price'] = request.POST['book_price_input']
		if 'course_number_input' in request.POST:	
			request.session['course_number'] = request.POST['course_number_input']
		# If user search by isbn, find the book and go directly to the confirm screen
		if len(isbn) != 0:
			# Check if the book with that isbn found, go to not found page if not found the book
			books = search_book(request)
			if len(books) != 0:
				# Redirect to confirm screen 
				book = books[0]
				if len(isbn) == 10:
					return HttpResponseRedirect("/book/sell/confirm?isbn=" + book.isbn10)
				elif len(isbn) == 13:
					return HttpResponseRedirect("/book/sell/confirm?isbn=" + book.isbn13)
			return render_to_response(
						"app/book/page/sell/sell_search_not_found.html",
						{
							'user_login': user_login,
							'new_notify': new_notify
						}
						,context_instance=RequestContext(request)) 
		# If not search by isbn, do the search normally
		else:
			books = search_book(request)		
			return render_to_response(
				"app/book/page/sell/sell_search.html",
				{
					'user_login': user_login,
					'new_notify': new_notify,
					'books': books
				}
				,context_instance=RequestContext(request))
	else:
		return render_to_response(
				"app/book/page/sell/sell_form.html",
				{
					'user_login': user_login,
					'new_notify': new_notify
				}
				,context_instance=RequestContext(request))




@login_required()
def sell_book_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if 'isbn' in request.GET:
		try:
			isbn = request.GET['isbn'].replace(" ","")
			book = None
			if len(isbn) == 10: 
				book = Book.objects.get(isbn10=isbn)
			elif len(isbn) == 13:
				book = Book.objects.get(isbn13=isbn)
			else:
				return HttpResponseRedirect('book/sell/error')
			request.session['book_isbn'] = book.isbn10
			course_number = None
			if 'course_number' in request.session:
				course_number = request.session['course_number']
			return render_to_response(
					"app/book/page/sell/sell_confirm.html",
					{
						'user_login': user_login,
						'new_notify': new_notify,
						'book': book,
						'book_price': request.session['book_price'],
						'book_condition': request.session['book_condition'],
						'course_number': course_number
						}
					,context_instance=RequestContext(request))
		except Book.DoesNotExist:
			return HttpResponseRedirect('book/sell/error')
	else:
		return HttpResponseRedirect('/book/sell/')

@login_required()
def sell_book_search(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	title = request.session['book_title']
	author =  request.session['book_author']
	books =  []
	if len(title) != 0 and len(author) != 0:
		books = get_book_by_title_and_author(title,author)
	else:
		if len(title) != 0:
			books = get_book_by_title(title)
		elif len(author) != 0:
			books = get_book_by_author(author)
	return render_to_response(
			"app/book/page/sell/sell_search.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'books': books
			}
			,context_instance=RequestContext(request))

@login_required()
def sell_book_action(request,book_isbn):
	book = get_object_or_404(Book,isbn10=book_isbn)
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
			"app/book/page/sell/sell_form.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'book': book,
				'price': request.session['book_price'],
				'condition': request.session['book_condition'],
				'course_number': request.session['course_number'],
			}
			,context_instance=RequestContext(request))

@login_required()
def sell_book_process(request):
	user_login = get_user_login_object(request)
	#try:
	books = Book.objects.filter(isbn10=request.session['book_isbn'])
	print books
	book = None
	if len(books) != 0:
		book = books[0]
	price = int(request.session['book_price'])
	condition = request.session['book_condition']
	alert_email = bool(int(request.session['alert_email']))
	book_sell = BookTransaction.objects.create(transaction_id=uuid.uuid1(),book=book,seller=user_login,price=price,condition=condition,transaction_type='1',alert_email=alert_email)
	#book_sell.transaction_id = uuid.uuid1()
	if request.session['course_number'] != None and len(request.session['course_number']) != 0:
		institution = user_login.institution_set.all()[0]
		course = None
		try:
			course = Course.objects.get(institution=institution,course_number=request.session['course_number'])
			if book not in course.course_book.all():
				course.course_book.add(book)
			course.save()
		except Course.DoesNotExist:
			course = Course.objects.create(institution=institution,course_number=request.session['course_number'])
			course.course_book.add(book)
			course.save()
		book_sell.course = course
	book_sell.save()
	if "book_condition" in request.session:
		del request.session['book_condition']
	if "alert_email" in request.session:
		del request.session['alert_email']
	if "book_isbn" in request.session:
		del request.session['book_isbn']
	if "course_number" in request.session:
		del request.session['course_number']
	if "book_price" in request.session:
		del request.session['book_price']
	return HttpResponseRedirect("/")
	#except:
	#	return HttpResponseRedirect('/book/sell/error')

@login_required()
def sell_book_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/sell_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)



@login_required()
def edit_sell_book(request):
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		try:
			user_login = get_user_login_object(request)
			new_notify = get_new_notify(request)
			transaction_id = request.GET['transaction_id']
			transaction = BookTransaction.objects.get(transaction_id=transaction_id)
			return render_to_response(
							"app/book/page/sell/edit_sell.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'transaction': transaction,
							}
							,context_instance=RequestContext(request)
						)
		except:
			return HttpResponseRedirect("/book/sell/delete/error")

@login_required()
def edit_sell_book_process(request):
	print "fgdgfd"
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/book/buy/item/edit/error")
	else:
		#try:
		transaction_id = request.GET['transaction_id']
		transaction = BookTransaction.objects.get(transaction_id=transaction_id)
		if request.GET['alert_email'] == '0':
			transaction.alert_email = False
		else:
			transaction.alert_email = True
		transaction.price = request.GET['price']
		transaction.condition = request.GET['condition']
		transaction.save()
		return HttpResponseRedirect("/")
		#except:
		#	return HttpResponseRedirect("/book/sell/edit/error")


@login_required()
def edit_sell_book_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/edit_sell_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

@login_required()
def delete_sell_book(request):
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		try:
			user_login = get_user_login_object(request)
			new_notify = get_new_notify(request)
			transaction_id = request.GET['transaction_id']
			transaction = BookTransaction.objects.get(transaction_id=transaction_id)
			return render_to_response(
							"app/book/page/sell/delete_sell.html",
							{
								"user_login": user_login,
								"new_notify": new_notify,
								'transaction': transaction,
							}
							,context_instance=RequestContext(request)
						)
		except:
			return HttpResponseRedirect("/book/sell/delete/error")

@login_required()
def delete_sell_book_process(request):
	if "transaction_id" not in request.GET:
		return HttpResponseRedirect("/")
	else:
		try:
			transaction_id = request.GET['transaction_id']
			transaction = BookTransaction.objects.get(transaction_id=transaction_id)
			for offer in transaction.offer.all():
				notifies = Notify.objects.filter(object_id=offer.pk)
				if len(notifies) != 0:
					for notify in notifies:
						notify.delete()
				offer.delete()
			transaction.delete()
			return HttpResponseRedirect("/")
		except:
			return HttpResponseRedirect("/book/sell/delete/error")

@login_required()
def delete_sell_book_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/sell/delete_sell_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)


########################################
#                                      #
#          TRADE / GIVE AWAY           #
#                                      #
########################################
@login_required()
def trade_give_book_form(request):
	new_notify = get_new_notify(request)
	user_login = get_user_login_object(request)
	if request.method == 'POST':
		isbn = request.POST['book_isbn_input']
		# If user search by isbn, find the book and go directly to the confirm screen
		if len(isbn) != 0:
			request.session['book_isbn'] = isbn
			request.session['book_condition'] = None
			request.session['alert_email'] = request.POST['alert_email_input']
			if "book_condition_input" in request.POST:
				request.session['book_condition'] = request.POST['book_condition_input']
			if 'course_number_input' in request.POST:	
				request.session['course_number'] = request.POST['course_number_input']
		
			# Check if the book with that isbn found, go to not found page if not found the book
			books = search_book(request)
			if len(books) != 0:
				# Redirect to confirm screen 
				book = books[0]
				return HttpResponseRedirect("/book/trade_give/confirm?isbn=" + book.isbn10)
			else:
				return render_to_response(
						"app/book/page/trade_give/trade_give_search_not_found.html",
						{
							'user_login': user_login,
							'new_notify': new_notify
						}
						,context_instance=RequestContext(request)) 
		# If not search by isbn, do the search normally
		else:
			books = search_book(request)		
			return render_to_response(
				"app/book/page/trade_give/trade_give_search.html",
				{
					'user_login': user_login,
					'new_notify': new_notify,
					'books': books
				}
				,context_instance=RequestContext(request))
	else:
		return render_to_response(
				"app/book/page/trade_give/trade_give_form.html",
				{
					'user_login': user_login,
					'new_notify': new_notify
				}
				,context_instance=RequestContext(request))

@login_required()
def trade_give_book_search(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	title = request.session['book_title']
	author =  request.session['book_author']
	books =  []
	if len(title) != 0 and len(author) != 0:
		books = get_book_by_title_and_author(title,author)
	else:
		if len(title) != 0:
			books = get_book_by_title(title)
		elif len(author) != 0:
			books = get_book_by_author(author)
	return render_to_response(
			"app/book/page/trade_give/trade_give_search.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'books': books
			}
			,context_instance=RequestContext(request))


@login_required()
def trade_give_book_confirm(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	if 'isbn' in request.GET:
		try:
			book = Book.objects.get(isbn10=request.GET['isbn'])
			request.session['book_isbn'] = book.isbn10
			course_number = None
			if 'course_number' in request.session:
				course_number = request.session['course_number']
			return render_to_response(
					"app/book/page/trade_give/trade_give_confirm.html",
					{
						'user_login': user_login,
						'new_notify': new_notify,
						'book': book,
						'book_condition': request.session['book_condition'],
						'course_number': course_number
						}
					,context_instance=RequestContext(request))
		except Book.DoesNotExist:
			return HttpResponseRedirect('book/trade_give/')
	else:
		return HttpResponseRedirect('/book/trade_give/')

@login_required()
def trade_give_book_action(request,book_isbn):
	book = get_object_or_404(Book,isbn10=book_isbn)
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
			"app/book/page/trade_give/trade_give_form.html",
			{
				'user_login': user_login,
				'new_notify': new_notify,
				'book': book,
			}
			,context_instance=RequestContext(request))

@login_required()
def trade_give_book_process(request):
	user_login = get_user_login_object(request)
	#try:
	book = Book.objects.get(isbn10=request.session['book_isbn'])
	condition = request.session['book_condition']
	alert_email = bool(int(request.session['alert_email']))
	book_trade_give = BookTransaction.objects.create(transaction_id=uuid.uuid1(),book=book,seller=user_login,condition=condition,transaction_type='2',alert_email=alert_email,price=0.00)
	#book_trade_give.transaction_id = uuid.uuid1()
	if len(request.session['course_number']) != 0:
		institution = user_login.institution_set.all()[0]
		course = None
		try:
			course = Course.objects.get(institution=institution,course_number=request.session['course_number'])
			if book not in course.course_book.all():
				course.course_book.add(book)
				course.save()
		except Course.DoesNotExist:
			course = Course.objects.create(institution=institution,course_number=request.session['course_number'])
			course.course_book.add(book)
			course.save()
		book_trade_give.course = course
	book_trade_give.save()
	if "book_condition" in request.session:
		del request.session['book_condition']
	if "alert_email" in request.session:
		del request.session['alert_email']
	if "book_isbn" in request.session:
		del request.session['book_isbn']
	if "course_number" in request.session:
		del request.session['course_number']
	return HttpResponseRedirect("/")
	#except:
	#	return HttpResponseRedirect('/book/trade_give/error')

@login_required()
def trade_give_book_error(request):
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	return render_to_response(
							"app/book/page/trade_give/trade_give_error.html",
							{
								"user_login": user_login,
								"new_notify": new_notify
							}
							,context_instance=RequestContext(request)
						)

