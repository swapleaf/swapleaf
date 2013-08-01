function invite_partner_callback(data) {
	//var message_el = $("#main_body").find('.alert-message')[0]
    var message_content = '<p class="notice-message">Your request has been sent. Please wait for response</p>';
    var message_el = '.alert-message'
    show_message(message_content,message_el);
    var btn_el = $("#main_body").find("#invite_" + data['username'])[0]
    $(btn_el).attr("onclick","");
    $(btn_el).attr('id','waiting_' + data['username']);
    $(btn_el).val("Pending Response");
    $(btn_el).addClass('disabled');
}

function delete_partner_callback(data) {
	//var message_el = $("#main_body").find('.alert-message')[0]
    var message_content = '<p class="notice-message">You have deleted the partnership with ' + data['firstname'] + " " + data['lastname'] + "</p>";
    var message_el = '.alert-message'
    show_message(message_content,message_el);
    var btn_el = $("#main_body").find("#delete_" + data['username'])[0]
    $(btn_el).attr("onclick","handle_invite_partner(this)");
    $(btn_el).attr('id','invite_' + data['username']);
    $(btn_el).val("Invite Partner");
}