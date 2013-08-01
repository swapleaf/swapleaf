$(document).ready(function () {

	$('.errorlist').each(function(index,value) {	
		var input_field = $($(this).parent()[0]).find('input')[0];
		$(input_field).css('border','1px solid red');
	})

	if ($('#id_state').find("option").length == 0) {
		var s = "<option value='None'>---Select the states---</option>" + USA_STATES_OPTION
		$('#id_state').html(s)
	}

	$('#id_state').change(function() {
  		var state_value = $(this).val()
  		if (state_value != 'None') {
  			Dajaxice.swapleaf.app.account.get_data_by_state(get_data_by_state_callback,{'state_value':state_value});
  		}
  		$($('#id_state').find('option[value="None"]')[0]).remove();
	});

	$('#id_city').change(function() {
  		var city_value = $(this).val()
  		var state_value = $('#id_state').val()
  		Dajaxice.swapleaf.app.account.get_institution_by_city(get_institution_by_city_callback,{'city_value':city_value,'state_value': state_value});
  		if (city_value == 'None') {
  			$('#id_institution option[value="None"]').attr('selected','selected');
  		}
	});

	$('.custom-validation-field').change(function() {
		var value = $(this).val()
  		if (value != 'None') {
			$(this).removeClass('error-field');
  		}
  		if (institution_select_validate()) {
  			$('.custom-validation-field').removeClass('error-field');
  			$('#id_zip_code').removeClass('error-field');
  			$('.institution-error').html("");
  		}
	})

	$('#signup_form').submit(function() {
		if (($('#id_institution').val() == "None") && ($('#id_zip_code').val() == "")) {
			var error_message = "Please select either your college/university or zip code";
			$('.institution-error').html(error_message);
			$('.custom-validation-field').addClass("error-field");
			$('#id_zip_code').addClass("error-field");
			return false;
		} else {
			$('.institution-error').html("");
			$('.custom-validation-field').removeClass("error-field");
			$('#id_zip_code').removeClass("error-field");
			return true;
		}
	})

})