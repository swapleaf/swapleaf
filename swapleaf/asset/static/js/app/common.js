// Autocomplete function for the searching
/*function search_autocomplete(data_src) {
    var data = new Array(); 
    for (var i = 0; i < data_src.length; i++) {
        var dt = new Object();
        dt.value = data_src[i]['name'];
        dt.id = data_src[i]['value'];
        dt.description = data_src[i]['description'];
        //dt.icon = data_src[i]['icon'];
        data.push(dt);
    }
    $("#search_query").autocomplete({
        source: data,
        minLength: 1,
        focus: function( event, ui ) {
            $( "#search_query" ).val( ui.item.value );  
            return false;
        },
        select: function( event, ui ) {
            $( "#search_query" ).val( ui.item.value );
                return false;
        }
    })
    .data( "autocomplete" )._renderItem = function( ul, item ) {
        var action_html = "";
        if (item.description == "People") {
            action_html = action_html + "<input type='button' id='invite_" + item.id + "' onclick='handle_invite_partner(this)' class='invite-btn btn btn-small btn-primary' value='Invite Partner'>";
        } 
        var inner_html = //'<a href="/' + item.id + '" >' + 
                              '<div class="autocomplete-item">' +
                                    '<div class="info pull-left">' + 
                                        '<a href="/' + item.id + '" >' +
                                            '<div class="title row-fluid">' + item.value + '</div>' +
                                            '<div class="description row-fluid">' + item.description + '</div>' +
                                        '</a>' + 
                                    '</div>' +
                                    '<div class="action pull-right">' +
                                        action_html + 
                                    '</div>' 
                              '</div>';
                          //'</a>';
        return $( "<li class='row-fluid'> </li>" ).data( "item.autocomplete", item ).append(inner_html).appendTo( ul );
    };
}*/

function handle_invite_partner(el) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else { 
        var el_id = $(el).attr('id')
        var username = el_id.substring(7,el_id.length);
        Dajaxice.swapleaf.app.friends.invite_partner(invite_partner_callback,{'username': username});
    }
}

function handle_delete_partner(el) {
    var user_login = $("#user_login").val();
    if (user_login == "None") {
        window.location.href = "/login";
    } else { 
        var el_id = $(el).attr('id')
        var username = el_id.substring(7,el_id.length);
        Dajaxice.swapleaf.app.friends.delete_partner(delete_partner_callback,{'username': username});
    }
}

function handle_view_listed_buy_item(isbn_value) {
    window.location.href = "/book/buy/search/isbn/listed/?book_isbn=" + isbn_value
}

function handle_offer_time_location(notify_id,offer_id,transaction_id) {
    window.location.href = "/offer/time_location/?offer_id=" + offer_id + "&notify_id=" + notify_id + "&transaction_id=" + transaction_id
}


function populateTime() {
    var hour_html = "";
    var minute_html = ""
    for (var i = 0; i < hour.length; i++) {
        hour_html = hour_html + "<option value=" + hour_dict[hour[i]] + ">" + hour[i] + "</option>"
    } 
    $("select[name='offer_hour_input']").html(hour_html)
    for (var i = 0; i < minute.length; i++) {
        minute_html = minute_html + "<option value=" + minute[i] + ">" + minute[i] + "</option>"
    } 
    $("select[name='offer_minute_input']").html(minute_html)
}
