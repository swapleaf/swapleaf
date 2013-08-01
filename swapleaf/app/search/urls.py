from django.conf.urls.defaults import *
from swapleaf import settings

urlpatterns = patterns('swapleaf.app.search.views',
    url(r"^$", "main_view"),
)
