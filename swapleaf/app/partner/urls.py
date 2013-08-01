from django.conf.urls.defaults import *
from swapleaf import settings

urlpatterns = patterns('swapleaf.app.partner.views',
    url(r"^$", "main_view"),
    url(r"^book/wanted/(?P<username>\w+)/$", "partner_book_wanted"),
    url(r"^book/available/(?P<username>\w+)/$", "partner_book_available"),
    url(r"^match/(?P<username>\w+)/$", "partner_book_match"),
    url(r"^others/match/(?P<username>\w+)/$", "partner_of_partner_match"),
)
