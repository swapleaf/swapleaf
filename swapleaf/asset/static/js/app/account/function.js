function institution_select_validate() {
	if (($('#id_institution').val() == "None") && ($('#id_zip_code').val() == "")) {
		return false;
	} 
	return true;
}