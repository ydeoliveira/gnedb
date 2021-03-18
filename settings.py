# Django settings for charazaynt project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
MANAGERS = ADMINS

DATABASES = {
    'default': {
'ENGINE':'django.db.backends.sqlite3',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
'NAME':'./gnedb.sqlite',             # Or path to database file if using sqlite3.
'USER':'',             # Not used with sqlite3.
'PASSWORD':'',         # Not used with sqlite3.
'HOST':'',             # Set to empty string for localhost. Not used with sqlite3.
'PORT':''             # Set to empty string for default. Not used with sqlite3.
}}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'players.apps.PlayersConfig'
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(os.path.abspath(__file__))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '15e*l8cu30hw5*)2%#-*cabgcp&olrt8%^^t9*6ijkvdo!i8nv'

# List of callables that know how to import templates from various sources.
"""TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)"""

TEMPLATES = [
			{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS' : [ os.path.join(PROJECT_PATH, 'templates/')],
			'APP_DIRS': True,
			'OPTIONS': {
				'context_processors': ['django.contrib.auth.context_processors.auth',
										'django.contrib.messages.context_processors.messages',
										'django.template.context_processors.debug',
										'django.template.context_processors.static',
										'django.template.context_processors.request']
				}
			}

]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
]

ROOT_URLCONF = 'urls'


"""TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates/')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)"""



LOGIN_REDIRECT_URL = '/'
