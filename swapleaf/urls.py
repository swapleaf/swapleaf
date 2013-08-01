from django.conf.urls import patterns, include, url
from django.conf import settings as settings
from django.contrib import admin

from allauth.account import views

#from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from dajaxice.core import dajaxice_autodiscover

from swapleaf import settings as swapleaf_settings
from swapleaf.app.account.forms import CustomSignupForm
from swapleaf.app.app_settings import SIGNUP_TEMPLATE, SIGNUP_SUCCESS_URL
from swapleaf.app.app_settings import LOGIN_TEMPLATE
from swapleaf.app.account import views as swapleaf_account_views
from swapleaf.app.member.views import settings as profile_settings_view
from swapleaf.settings import LOGOUT_REDIRECT_URL

from tastypie.api import Api

dajaxice_autodiscover()
admin.autodiscover()

frittie_api = Api(api_name='swapleaf')

urlpatterns = patterns('',
    # Admin URL
    url(r'^admin/', include(admin.site.urls)),

    # Allauth app URL
    #url(r'^accounts/', include('allauth.urls')),
    url(r"^signup/$",   swapleaf_account_views.signup, 
                        {
                            'template_name': SIGNUP_TEMPLATE,
                            'success_url': SIGNUP_SUCCESS_URL,
                            'form_class': CustomSignupForm 
                        }
                        , name="account_signup"),
    url(r"^login/$",    swapleaf_account_views.login,   
                        {
                            'template_name': LOGIN_TEMPLATE
                        }
                        , name="account_login"),
    # url(r"^login/$", views.login,   {
    #                                     'template_name': LOGIN_TEMPLATE
    #                                 }
    #                                 , name="account_login"),
    url(r"^password/change/$", views.password_change, {'template_name': 'app/account/password_change.html'}, name="account_change_password"),
    url(r"^password/set/$", views.password_set, name="account_set_password"),
    url(r"^logout/$", views.logout, {
                                        'next_page': LOGOUT_REDIRECT_URL,
                                    }
                                    , name="account_logout"),
    url(r"^password/reset/$", views.password_reset, name="account_reset_password"),
    url(r"^password/reset/done/$", views.password_reset_done, name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key, name="account_reset_password_from_key"),

    # Haystack URL
    #(r'^search/', include('haystack.urls')),

    url(r"^search/$",include('swapleaf.app.search.urls')),

    # Custom Account URL
    url(r'^confirmation/(?P<confirmation_key>\w+)/',swapleaf_account_views.confirmation, name="account_email_confirmation"),

    # SwapLeaf URL
    url(r'^$', include('swapleaf.app.main.urls')),
    url(r'^settings/$', profile_settings_view),
    url(r'^book/', include('swapleaf.app.book.urls')),
    url(r'^offer/', include('swapleaf.app.offer.urls')),
    url(r'^partner/', include('swapleaf.app.partner.urls')),
    url(r"^notification/",include('swapleaf.app.notify.urls')),

    # Dajaxice URL
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^%s/' % swapleaf_settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Media URL
    url(r'^asset/media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    
    # Final URL - Member page
    url(r'^(?P<username>\w+)/',include('swapleaf.app.member.urls')),
)


