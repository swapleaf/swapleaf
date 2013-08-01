function accept_partner_callback(data) {
    if (data['reload'] == 'True') {
        location.reload()
    } else {
        var new_content = data['new_content']
        var notify_el = "#notify-" + data['notify_id'] + " .notify-content"
        $(notify_el).html(new_content)
        var s = '<p class="notice-message">You are now partner with <a href=/' + 
                data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
        var el = '.alert-message'
        show_message(s,el)
    }
}

function decline_partner_callback(data) {
    if (data['reload'] == 'True') {
        location.reload()
    } else {
        var new_content = data['new_content']
        var notify_el = "#notify-" + data['notify_id'] + " .notify-content"
        $(notify_el).html(new_content)
        var s = '<p class="notice-message">You have declined partner request of <a href=/' + 
                data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
        var el = '.alert-message'
        show_message(s,el)
    }
}
