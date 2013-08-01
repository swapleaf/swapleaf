function showEmptyError(el,red_border) {
	if (red_border) {
		$(el).css('border',"1px solid red");
	}
	var error_el = $($(el).parent()).find(".error")[0];
	$(error_el).show();
	$(error_el).html("This field is required");
}

function clearEmptyError(el,red_border) {
	if (red_border) {
		$(el).css('border',"1px solid #ccc");
	}	
	var error_el = $($(el).parent()).find(".error")[0];
	$(error_el).hide();
	$(error_el).html("");
}

function checkISBNField() {
	if ($("#book_isbn_input").val().length == 0) {
		showEmptyError('#book_isbn_input',true)
		return false;
	} else {
		clearEmptyError('#book_isbn_input',true)
		return true;
	}
}

function checkPriceField() {
	if ($("#book_price_input").val().length == 0) {
		showEmptyError('#book_price_input',true)
		return false;
	} else {
		clearEmptyError('#book_price_input',true)
		return true;
	}
}

function checkConditionField() {
	var condition = $(".book-condition input[name='book_condition_input']:checked").val()
	if (!condition) {
		showEmptyError('.book-condition .input-field',false)
		return false;
	} else {
		clearEmptyError('.book-condition .input-field',false)
		return true;
	}
}

function handle_search_sell_book(el) {
	var title = $("#book_title_input").val()
	var author = $("#book_author_input").val()
	var price = $("#book_price_input").val()
	var condition = $("input[name='book_condition_input']:checked","#sell_book_form").val()
	if (!condition) {
		condition = null
	}
	var course_number = $("#course_number_input").val()
	//var alert_email= $('#alert_email_input').val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	Dajaxice.swapleaf.app.book.handle_search_sell_book(handle_search_sell_book_callback, 
						{
							"title": title,
							"author": author,
							"price": price,
							"condition": condition,
							"course_number": course_number,
							'alert_email': alert_email
						}
					)
}

function handle_search_trade_give_book(el) {
	var title = $("#book_title_input").val()
	var author = $("#book_author_input").val()
	var condition = $("input[name='book_condition_input']:checked","#sell_book_form").val()
	if (!condition) {
		condition = null
	}
	var course_number = $("#course_number_input").val()
	//var alert_email= $('#alert_email_input').val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	Dajaxice.swapleaf.app.book.handle_search_trade_give_book(handle_search_trade_give_book_callback, 
						{
							"title": title,
							"author": author,
							"condition": condition,
							"course_number": course_number,
							"alert_email": alert_email,
						}
					)
}

function handle_search_title_author_buy_book(el) {
	var title = $("#book_title_input").val()
	var author = $("#book_author_input").val()
	//var alert_email= $('#alert_email_input').val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	Dajaxice.swapleaf.app.book.handle_search_title_author_buy_book(handle_search_title_author_buy_book_callback, 
						{
							"title": title,
							"author": author,
							"alert_email": alert_email,
						}
					)
	/*var title = $("#book_title_input").val()
	var author = $("#book_author_input").val()
	window.location.href = '/book/buy/search/title_author/?title=' + title + "&author=" + author*/
}

function handle_search_available_book_author(el) {
	var author = $("#available_book_author_input").val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	Dajaxice.swapleaf.app.book.handle_search_available_book_author(handle_search_available_book_author_callback, 
						{
							"author": author,
							"alert_email": alert_email,
						}
					)
}

function handle_course_buy_book(el) {
	var course_number = $("#course_number_input").val()
	//var alert_email= $('#alert_email_input').val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	var school_id = $("#school_id").val()
	Dajaxice.swapleaf.app.book.handle_course_buy_book(handle_course_buy_book_callback, 
						{
							"course_number": course_number,
							"alert_email": alert_email,
							"school_id": school_id,
						}
					)
	/*var course_number = $("#course_number_input").val()
	var school_id = $("#school_id").val()
	window.location.href = "/book/buy/search/course/?course_number=" + course_number + "&school_id=" + school_id*/
}


function handle_search_isbn_buy_book(el) {
	var isbn = $("#book_isbn_input").val()
	//var alert_email= $('#alert_email_input').val()
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	Dajaxice.swapleaf.app.book.handle_search_isbn_buy_book(handle_search_isbn_buy_book_callback, 
						{
							"isbn": isbn,
							"alert_email": alert_email,
						}
					)
	/*window.location.href = "/book/buy/search/isbn/" + isbn*/
}

function handle_select_buy_item(isbn_value) {
	window.location.href = "/book/buy/add_item/process/" + isbn_value
}

function handle_edit_buy_book(el) {
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	var buy_book_id = $("#buy_book_id").val()
	window.location.href='/book/buy/item/edit/process/?alert_email='+alert_email+"&buy_book_id=" + buy_book_id
}

function handle_edit_sell_book(el) {
	var alert_email =  $($('input[name=alert_email_input]:checked')[0]).val();
	var condition = $($('input[name=book_condition_input]:checked')[0]).val();
	//console.log(condition)
	var price = $("#book_price_input").val()
	var transaction_id = $("#transaction_id").val()
	window.location.href='/book/sell/edit/process/?alert_email='+alert_email+"&condition="+condition+"&price="+price+"&transaction_id=" + transaction_id
}
