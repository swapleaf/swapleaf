from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response

from swapleaf.helper.common import get_user_login_object, handle_request_get_message, get_new_notify
from swapleaf.helper.common import get_autocomplete_data, remove_duplicate_object
from swapleaf.helper.book import get_book_by_isbn, get_book_by_title, get_book_by_author
from swapleaf.helper.account import get_people_by_name
from swapleaf.helper.member import check_partnership

# Create your views here.
def main_view(request):
	message = handle_request_get_message(request)
	autocomplete_data = get_autocomplete_data(request)
	user_login = get_user_login_object(request)
	new_notify = get_new_notify(request)
	books = []
	people = []
	if request.method == "GET":
		if "q" in request.GET:
			query = request.GET['q']
			if len(query) != 0:
				book_by_isbn = get_book_by_isbn(query)
				book_by_title = get_book_by_title(query)
				book_by_author = get_book_by_author(query)
				books = remove_duplicate_object(book_by_isbn + book_by_title + book_by_author)
				people = get_people_by_name(request,query)
				for person in people:
					person.get_profile().partner_status = check_partnership(request,person.username)
					person.get_profile().save()
	return render_to_response(
			"app/search/page/main_view.html",
			{
				'message': message,
				'autocomplete_data': autocomplete_data,
				'user_login': user_login,
				'books': books,
				'people': people,
				'new_notify': new_notify,
			},
			context_instance=RequestContext(request)
		)