function handle_accept_partner(notify_id) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else {
        var username = $("#get_username_notify_" + notify_id).val()
        Dajaxice.swapleaf.app.friends.accept_partner(accept_partner_callback,{"username":username, "notify_id": notify_id})
    }
}

function handle_decline_partner(notify_id) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else {
        var username = $("#get_username_notify_" + notify_id).val()
        Dajaxice.swapleaf.app.friends.decline_partner(decline_partner_callback,{"username":username, "notify_id": notify_id})
    }
}

function handle_accept_offer_confirm(notify_id,offer_id,transaction_id) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else {
        window.location.href = "/offer/accept/price/confirm/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
    }
}

function handle_make_counter_offer(notify_id,offer_id,transaction_id) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else {
       /* var link = "/book/offer/counter/" + offer_id + "/?transaction_id=" + transaction_id
        console.log(link)*/
        window.location.href = "/offer/counter/price/" + offer_id + "/?transaction_id=" + transaction_id
    }
}

function handle_decline_offer(notify_id,offer_id,transaction_id) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else {
        window.location.href = "/offer/price/decline/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
    }
}

function handle_make_another_suggestion(notify_id,offer_id,transaction_id) {
     window.location.href = "/offer/time_location/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
}

function handle_accept_suggestion_confirm(notify_id,offer_id,transaction_id) {
     window.location.href = "/offer/accept/time_location/confirm/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
}