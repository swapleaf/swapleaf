from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Q

from swapleaf.app.main.models import BookTransaction, Book, Course, Institution
from swapleaf.app.app_settings import IGNORE_WORDS
from swapleaf.helper.common import convert_queryset_to_list, remove_duplicate_object, get_user_login_object
from swapleaf.helper.common import remove_duplicate_object

import urllib2
import json

# Get the book with format like: "http://openlibrary.org/api/books?bibkeys=ISBN:" + isbn + "&jscmd=details&format=json"
def search_book_online_by_isbn(isbn):
	if len(isbn) == 10:
		books = Book.objects.filter(isbn10=isbn)
		if len(books) != 0:
			book = books[0]
			for i in range(1,len(books)):
				books[i].delete()
			return book
	else:
		books = Book.objects.filter(isbn13=isbn)
		if len(books) != 0:
			book = books[0]
			for i in range(1,len(books)):
				books[i].delete()
			return book
	isbn = isbn.replace(" ","")
	link = "http://openlibrary.org/api/books?bibkeys=ISBN:" + isbn + "&jscmd=details&format=json"
	print link
	data = urllib2.urlopen(link)
	a = data.read()
	json_data = json.loads(a)
	if len(json_data) != 0:
		new_book = Book()
		if 'table_of_contents' in json_data['ISBN:' + isbn]['details']:
			new_book.title = json_data['ISBN:' + isbn]['details']['table_of_contents'][0]['title']
		else:
			new_book.title = json_data['ISBN:' + isbn]['details']['title']
		if len(isbn) == 10:
			new_book.isbn10 = isbn
			if "isbn_13" in json_data['ISBN:' + isbn]['details']:
				new_book.isbn13 = json_data['ISBN:' + isbn]['details']['isbn_13'][0]
		else:
			new_book.isbn13 = isbn
			if "isbn_10" in json_data['ISBN:' + isbn]['details']:
				new_book.isbn10 = json_data['ISBN:' + isbn]['details']['isbn_10'][0]
		if "authors" in json_data['ISBN:' + isbn]['details']:
			for i in range(0,len(json_data['ISBN:' + isbn]['details']['authors'])):
				if i == 0:
					new_book.author = new_book.author + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
				else:
					new_book.author = new_book.author + ", " + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
		if "revision" in json_data['ISBN:' + isbn]['details']:
			new_book.edition = json_data['ISBN:' + isbn]['details']['revision']
		new_book.save()
		return new_book
	else:
		return None

# Get the book with format like: http://openlibrary.org/books/OL20943166M.json
def get_openlibrary_book(book_query):
	link = "http://openlibrary.org" + book_query + ".json"
	data = urllib2.urlopen(link)
	a = data.read()
	json_data = json.loads(a)
	#print json_data
	if len(json_data) != 0:
		if "isbn_10" in json_data:
			return search_book_online_by_isbn(json_data['isbn_10'][0])
		elif "isbn_13" in json_data:
			return  search_book_online_by_isbn(json_data['isbn_13'][0])
		else:
			return None 
	else:
		return None

def get_book_by_course(request,course_number,school_id):
	user_login = get_user_login_object(request)
	courses = Course.objects.filter(course_number__iexact=course_number,institution=Institution.objects.get(id=school_id))
	if len(courses) == 0:
		return []
	else:
		course = courses[0]
		books = convert_queryset_to_list(course.course_book.all())
		result = []
		for book in books:
			b = BookTransaction.objects.filter(seller=user_login,book=book)
			if len(b) == 0:
				result.append(book)
		return remove_duplicate_object(result)

def get_book_by_isbn(query):
	if query == None:
		return []
	isbn_str = query.split()[0].replace(" ","")
	books = []
	if len(isbn_str) == 10:
		books = convert_queryset_to_list(Book.objects.filter(isbn10__iexact=isbn_str))
		if len(books) == 0:
			new_book = search_book_online_by_isbn(isbn_str)
			if new_book != None:
				books.append(new_book)
	elif len(isbn_str) == 13:
		books = convert_queryset_to_list(Book.objects.filter(isbn13__iexact=isbn_str))
		if len(books) == 0:
			new_book = search_book_online_by_isbn(isbn_str)
			if new_book != None:
				books.append(new_book)
	return remove_duplicate_object(books)

def get_book_by_title(query):
	title_words = query.split()
	books = Book.objects.filter(title=query)
	if len(books) != 0:
		return convert_queryset_to_list(books)
	else:
		result = []
		for title_word in title_words:
			if title_word.lower() not in IGNORE_WORDS:
				books = convert_queryset_to_list(Book.objects.filter(title__icontains=title_word))
				result = result + books
		return remove_duplicate_object(result)
	# lst = [word[0].upper() + word[1:] for word in query.split()]
	# title_name = " ".join(lst).replace(" ","+")
	# title_link = "http://openlibrary.org/query.json?type=/type/edition&title=" + title_name
	# title_request = urllib2.urlopen(title_link)
	# title_data = title_request.read()
	# title_json = json.loads(title_data)
	# database = Book.objects.filter(title=query)
	# #print len(database)
	# if len(database) >= len(title_json):
	# 	return convert_queryset_to_list(database)
	# result = []
	# if len(title_json) != 0:
	# 	for book_item in title_json:
	# 		book_query = book_item['key']
	# 		print book_query
	# 		book = get_openlibrary_book(book_query)
	# 		if book != None:
	# 			result.append(book)
	# return remove_duplicate_object(result)

def get_book_by_author(query):
	author_words = query.split()
	books = Book.objects.filter(author=query)
	if len(books) != 0:
		return convert_queryset_to_list(books)
	else:
		result = []
		for author_word in author_words:
			if author_word.lower() not in IGNORE_WORDS:
				print author_word
				books = convert_queryset_to_list(Book.objects.filter(author__icontains=author_word))
				result = result + books
		return remove_duplicate_object(result)
	# lst = [word[0].upper() + word[1:] for word in query.split()]
	# author_name = " ".join(lst).replace(" ","+")
	# author_link = "http://openlibrary.org/query.json?type=/type/author&name=" + author_name
	# author_request = urllib2.urlopen(author_link)
	# author_data = author_request.read()
	# author_json = json.loads(author_data)
	# result = []
	# if len(author_json) != 0:
	# 	for item in author_json:
	# 		author_id = item['key']
	# 		book_link = "http://openlibrary.org/query.json?type=/type/edition&authors=" + author_id
	# 		book_request = urllib2.urlopen(book_link)
	# 		book_data = book_request.read()
	# 		book_json = json.loads(book_data)
	# 		print len(book_json)
	# 		for book_item in book_json:
	# 			book_query = book_item['key']
	# 			book = get_openlibrary_book(book_query)
	# 			if book != None:
	# 				result.append(book)
	# return remove_duplicate_object(result)

def get_book_by_title_and_author(title_query,author_query):
	title_words = title_query.split()
	author_words = author_query.split()
	result = []
	for title_word in title_words:
		for author_word in author_words:
			if title_word.lower() not in IGNORE_WORDS and author_word.lower() not in IGNORE_WORDS:
				books = convert_queryset_to_list(Book.objects.filter(title__icontains=title_word,author__icontains=author_word))
				result = result + books
	return remove_duplicate_object(result)

def search_book(request):
	isbn = request.POST['book_isbn_input']
	title = request.POST['book_title_input']
	author =  request.POST['book_author_input'] 
	if len(isbn) != 0:
		return get_book_by_isbn(isbn)
	elif len(title) != 0:
		return get_book_by_title(title)
	elif len(author) != 0:
		return get_book_by_author(author)
	else:
		return []

def get_authors(query):
	lst = [word[0].upper() + word[1:] for word in query.split()]
	author_name = " ".join(lst).replace(" ","+")
	author_link = "http://openlibrary.org/query.json?type=/type/author&name=" + author_name
	author_request = urllib2.urlopen(author_link)
	author_data = author_request.read()
	author_json = json.loads(author_data)
	result = []
	if len(author_json) != 0:
		for item in author_json:
			author_id = item['key']
			author_item_link = "http://openlibrary.org" + author_id + ".json"
			print author_item_link
			author_item_request = urllib2.urlopen(author_item_link)
			author_item_data = author_item_request.read()
			author_item_json = json.loads(author_item_data)
			if 'name' in author_item_json:
				author_item_name = author_item_json['name']
				result.append(author_item_name)
	return remove_duplicate_object(result)

# temporary logic - just get all book for right now
# def search_book(request):
# 	isbn = request.POST['book_isbn_input']
# 	title = request.POST['book_title_input']
# 	author =  request.POST['book_author_input'] 
# 	if len(isbn) != 0:
# 		return get_book_by_isbn(isbn)
# 		isbn_str = isbn.split()[0]
# 		books = []
# 		if len(isbn_str) == 10:
# 			books = Book.objects.filter(isbn10__iexact=isbn_str)
# 		elif len(isbn_str) == 13:
# 			books = Book.objects.filter(isbn13__iexact=isbn_str)
# 		return books
# 	elif len(title) != 0:
# 		return get_book_by_title(title)
# 		title_words = title.split()
# 		result = []
# 		for word in title_words:
# 			if word.lower() not in IGNORE_WORDS:
# 				books = convert_queryset_to_list(Book.objects.filter(title__icontains=word))
# 				result = result + books
# 		return result
# 	elif len(author) != 0:
# 		return get_book_by_author(author)
# 		author_words = author.split()
# 		result = []
# 		for word in author_words:
# 			if word.lower() not in IGNORE_WORDS:
# 				books = convert_queryset_to_list(Book.objects.filter(author__icontains=word))
# 				result = result + books
# 		return result
# 	else:
# 		return []

# 	book_sells = BookTransaction.objects.all()
# 	book_trades_gives = BookTradingGiving.objects.all()
# 	book_trades = BookTrading.objects.all()
# 	book_gives = BookGiving.objects.all()
# 	result = []
# 	for book_sell in book_sells:
# 		buy_book_item = BookBuying.objects.create(book=book_sell.book, \
# 				transaction_type = "sell", transaction_partner = book_sell.seller,
# 				price = book_sell.price, post_time = book_sell.post_time
# 			)
# 		buy_book_item.save()
# 		result.append(buy_book_item)
# 	for book_trade_give in book_trades_gives:
# 		buy_book_item = BookBuying.objects.create(book=book_trade_give.book1, \
# 				transaction_type = "trade_give", transaction_partner = book_trade_give.trader1_giver,
# 				price = 0.00, post_time = book_trade_give.post_time
# 			)
# 		buy_book_item.save()
# 		result.append(buy_book_item)
# 	for book_give in book_gives:
# 		buy_book_item = BookBuying.objects.create(book=book_give.book, \
# 				transaction_type = "give_away", transaction_partner = book_give.giver,
# 				price = 0.00, post_time = book_give.post_time
# 			)
# 		buy_book_item.save()
# 		result.append(buy_book_item)
# 	return result

