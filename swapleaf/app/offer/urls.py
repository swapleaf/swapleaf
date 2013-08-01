from django.conf.urls.defaults import *
from swapleaf import settings

urlpatterns = patterns('swapleaf.app.offer.views',
    url(r"^price/$","offer_price_form"),
    url(r'^price/process/$','offer_price_process'),
    url(r"^time_location/$","offer_time_location_form"),
    url(r'^time_location/process/$','offer_time_location_process'),
    url(r'^price/success/$','offer_price_success'),
    url(r'^time_location/success/$','offer_time_location_success'),
    url(r'^error/$','offer_error'),
    url(r'^counter/price/(?P<offer_id>\d+)/$','counter_offer_price_form'),
    url(r'^counter/price/process/$','counter_offer_price_process'),
    url(r'^counter/price/check/$','counter_offer_price_check'),
    # url(r'^counter/time_location/(?P<offer_id>\d+)/$','counter_offer_time_location_form'),
    # url(r'^counter/time_location/process/$','counter_offer_time_location_process'),
    url(r'^accept/price/confirm/$','accept_offer_price_confirm'),
    url(r'^accept/price/process/$','accept_offer_price_process'),
    url(r'^accept/time_location/confirm/$','accept_offer_time_location_confirm'),
    url(r'^accept/time_location/process/$','accept_offer_time_location_process'),
    url(r'^decline/$','decline_offer'),
)
