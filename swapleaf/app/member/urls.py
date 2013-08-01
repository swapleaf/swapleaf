from django.conf.urls.defaults import *
from swapleaf import settings

urlpatterns = patterns('swapleaf.app.member.views',
    url(r"^$", "main_view"),
)
