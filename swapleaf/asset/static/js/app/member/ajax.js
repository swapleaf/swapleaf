function get_data_by_state_callback(data) {
	var list_city = []
	var city = "<option value='None'>---Select the city---</option>";
	var institution = "<option value='None'>---Select the institution---</option>";
	for (var i = 0; i < data.length; i++) {
		if ($.inArray(data[i][0], list_city) == -1) {
			list_city.push(data[i][0]);
		}
		institution = institution + "<option value='" + data[i][2] + "'>" + data[i][1] + "</option>";
	}
	list_city.sort();
	for (var i = 0; i < list_city.length; i++) {
		city = city + "<option value='" + list_city[i] + "'>" + list_city[i] + "</option>";
	}
	$('#id_city').html(city);
	$('#id_institution').html(institution);
	$(".city-field").show();
	$(".institution-field").show();
}

function get_institution_by_city_callback(data) {
	var institution = "<option value='None'>---Select the institution---</option>";
	for (var i = 0; i < data.length; i++) {
		institution = institution + "<option value='" + data[i][1] + "'>" + data[i][0] + "</option>";
	}
	$('#id_institution').html(institution);
	$(".institution-field").show();
}
