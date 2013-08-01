# Django settings for swapleaf project.

import os
ROOT_PATH = os.path.dirname(__file__)
#WEBSITE_HOMEPAGE = "http://swapleaf.com/"
WEBSITE_HOMEPAGE = "http://localhost:8000/"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'swapleafadmin'
EMAIL_HOST_USER = 'swapleaf@gmail.com'
EMAIL_USE_TLS = True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'swapleaf.sql',
        'USER': 'postgres',                      
        'PASSWORD': '123456',                  
        'HOST': 'localhost',                 
        'PORT': '5432',                      
    }
}

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'd121ffb4i2qkss',
#     'HOST': 'ec2-54-243-243-216.compute-1.amazonaws.com',
#     'PORT': 5882,
#     'USER': 'ucnqgrj3jjr4ur',
#     'PASSWORD': 'p539j1m9atf4os7551gtj4umgmo'
#   }
# }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'asset/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = WEBSITE_HOMEPAGE + "asset/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.abspath(ROOT_PATH), 'asset/static'),   
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'oaf1o0g80gfu9k+57c#!bw8k+fic_q-h4z5b+%29^^6hcp3=l)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.request",
    'allauth.account.context_processors.account',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'swapleaf.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'swapleaf.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, "asset/templates"),
)

FIXTURE_DIRS = (
    os.path.join(ROOT_PATH, "fixtures"),
)

INSTALLED_APPS = (
    # Django built-in apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Frittie app 
    'swapleaf.app',
    'swapleaf.app.main',
    'swapleaf.app.account',
    'swapleaf.app.member',
    'swapleaf.app.book',
    'swapleaf.app.friends',
    'swapleaf.app.search',
    'swapleaf.app.notify',
    'swapleaf.app.offer',
    'swapleaf.app.partner',
    'swapleaf.helper',

    # Allauth app
    'allauth',
    'allauth.account',

    # Others app
    'dajaxice',
    'tastypie',
    'haystack',
    'south',
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
)
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile_dajaxice': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "log/dajaxice.log"),
        }, 
        'logfile_facebook': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "log/django_facebook.log"),
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'dajaxice': {
            'handlers': ['logfile_dajaxice'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_facebook':{
            'handlers': ['logfile_facebook'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }, 
}

AUTH_PROFILE_MODULE = 'main.UserProfile'

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend', 
)

ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 4
ACCOUNT_EMAIL_VERIFICATION = False

DAJAXICE_MEDIA_PREFIX="dajaxice"

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

HAYSTACK_SITECONF = 'swapleaf.app.search.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(ROOT_PATH, 'db/whoosh/')
HAYSTACK_USE_REALTIME_SEARCH = False

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://postgres:123456@localhost:5432/swapleaf.sql')}
