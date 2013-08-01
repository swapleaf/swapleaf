/*function handle_book_action_callback(data) {
	$('.display-area').html(data['snippet_content']);
}*/

function handle_search_sell_book_callback(data) {
	window.location.href='/book/sell/search/'
}

function handle_search_trade_give_book_callback(data) {
	window.location.href='/book/trade_give/search/'
}

function handle_search_title_author_buy_book_callback(data) {
	window.location.href='/book/buy/search/title_author/'
}

function handle_course_buy_book_callback(data) {
	window.location.href='/book/buy/course/confirm'
}

function handle_search_isbn_buy_book_callback(data) {
	window.location.href='/book/buy/search/isbn/' + data['isbn']
}

function handle_search_available_book_author_callback(data) {
	window.location.href = '/book/buy/author/available_book/confirm'
}