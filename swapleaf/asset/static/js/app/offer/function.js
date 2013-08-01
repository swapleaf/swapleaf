function handle_accept_offer_process(notify_id,offer_id,transaction_id) {
    window.location.href = "/offer/accept/price/process/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
}

function handle_accept_suggestion_process(notify_id,offer_id,transaction_id) {
   window.location.href = "/offer/accept/time_location/process/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
}
