# Define all the settings for the swapleaf app here
SESSION_KEY = '_auth_user_id'

SIGNUP_TEMPLATE = "app/account/page/signup.html"
SIGNUP_SUCCESS_URL = "/?action=signup&result=success"

LOGIN_TEMPLATE = "app/account/page/login.html"

MESSAGE_SNIPPET_TEMPLATE = 	{	
								"signup_success": "text/message/signup_success.html",
								"signup_error": "text/message/signup_error.html",
								"confirm_email_success": "text/message/confirm_email_success.html",
								"confirm_email_error": "text/message/confirm_email_error.html",
								"confirm_email_asking": "text/message/confirm_email_asking.html"
							}

NOTIFY_SNIPPET_TEMPLATE = 	{	
								"invite_partner": "text/notify/partner/invite_partner.html",
								'accept_partner': "text/notify/partner/accept_partner.html",
								'invite_partner_response_accept': "text/notify/partner/invite_partner_response_accept.html",
								'invite_partner_response_decline': "text/notify/partner/invite_partner_response_decline.html",
								"make_offer_price_normal_content": "text/notify/offer/make_offer_price_normal_content.html",
								"make_offer_price_offer_content": "text/notify/offer/make_offer_price_offer_content.html",
								'make_counter_offer_price':'text/notify/offer/make_counter_offer_price.html',
								'counter_offer_price_notice_normal_content':'text/notify/offer/counter_offer_price_notice_normal_content.html',
								'counter_offer_price_notice_offer_content':'text/notify/offer/counter_offer_price_notice_offer_content.html',
								'accept_offer_price':'text/notify/offer/accept_offer_price.html',
								'accept_offer_price_notice':'text/notify/offer/accept_offer_price_notice.html',
								"make_offer_time_location": "text/notify/offer/make_offer_time_location.html",
								'accept_offer_time_location':'text/notify/offer/accept_offer_time_location.html',
								'accept_offer_time_location_notice':'text/notify/offer/accept_offer_time_location_notice.html',
							}


IGNORE_WORDS = ['the','a','an','this','that','there',
				'they','in','their','and','or','&',
				'we','he','she','i','you','are','is',
				'it','of','at','on','to','what','where',
				'when','why','who','how','be','for','from',
				'not']