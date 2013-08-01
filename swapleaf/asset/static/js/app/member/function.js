function institution_select_validate() {
	if ($("#has_college").val() == "True") {
		return true;
	} else {
		if (($('#id_institution').val() == "None") && ($('#id_zip_code').val() == "")) {
			return false;
		} 
		return true;
	}
}