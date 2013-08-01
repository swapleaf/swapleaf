from django.conf.urls.defaults import *

urlpatterns = patterns('swapleaf.app.notify.views',
	url(r"^$", "show_all_notification"),
	url(r"^offer/$","show_offer_notification"),
	url(r"^error/$","notification_error"),

)

