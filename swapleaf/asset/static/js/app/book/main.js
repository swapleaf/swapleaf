$(document).ready(function () {
	/*$('.book-action-btn').click(function() {
  		var action_value = $(this).val();
  		Dajaxice.swapleaf.app.book.handle_book_action(handle_book_action_callback,{'action_value': action_value});
	});*/

	$('#sell_book_form').submit(function() {
		var check = true;
		if (!checkISBNField()) {
			check = false;
		}
		if (!checkConditionField()) {
			check = false;
		}
		if (!checkPriceField()) {
			check = false;
		}
		return check;
	})

	$('#trade_give_book_form').submit(function() {
		var check = true;
		if (!checkISBNField()) {
			check = false;
		}
		if (!checkConditionField()) {
			check = false;
		}	
		return check;
	})
	//populateDate();
	populateTime();
})