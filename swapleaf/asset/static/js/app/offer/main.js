$(document).ready(function() {
	$("#datepicker").datepicker({
		changeMonth: true,
        changeYear: true,
        minDate: 1, maxDate: "+4M"
	})
	populateTime()
})