"""
Base settings and globals.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the config directory:
CONFIG_ROOT = dirname(abspath(__file__))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(CONFIG_ROOT)

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = dirname(PROJECT_ROOT)

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project folder:
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Project domain:
PROJECT_DOMAIN = '%s.com' % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(CONFIG_ROOT)
path.append(PROJECT_ROOT)
path.append(os.path.join(PROJECT_ROOT, 'apps'))
# import pdb; pdb.setb_trace()
########## END PATH CONFIGURATION


########## EMAIL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_NAME

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'Serverbot <dev@%s>' % PROJECT_DOMAIN
########## END EMAIL CONFIGURATION


########## MANAGER CONFIGURATION
# See https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Dev Team', 'Dev Team <dev@%s>' % PROJECT_DOMAIN),
)

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'test_without_migrations',
)

PROJECT_APPS = (
    'elastic_haystack',
    'elastic_json',
    'elastic_api',
    'elastic_dsl',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS
########## END APP CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## MIGRATIONS CONFIGURATION
MIGRATION_MODULES = {
    'sites': 'extensions.sites.migrations'
}
########## END MIGRATIONS CONFIGURATION


########## DEBUG CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = STAGING = False
########## END DEBUG CONFIGURATION


########## SECRET CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"lle*l7qn&!tog)$1n$=#op1rst%e!7k8t-k@wmjjv@msnuo6ud"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(PROJECT_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## GENERAL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Kiev'

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(PROJECT_ROOT, 'templates')),
            normpath(join(PROJECT_ROOT, 'extensions')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'string_if_invalid': 'NULL',
        },
    },
]
########## END TEMPLATE CONFIGURATION


########## MEDIA CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'assets'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PROJECT_ROOT, 'static')),
)

# STATICFILES_FINDERS_IGNORE = [
#     '*.scss',
#     '*.coffee',
#     '*.map',
#     '*.html',
#     '*.txt',
#     '*tests*',
#     '*uncompressed*',
# ]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

########## URL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'urls'
########## END URL CONFIGURATION


########## LOGIN/LOGOUT CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = '/login/'

# https://docs.djangoproject.com/en/dev/ref/settings/#logout-url
LOGOUT_URL = '/logout/'
########## END LOGIN/LOGOUT CONFIGURATION


########## WSGI CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## TESTING CONFIGURATION
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
########## END TESTING CONFIGURATION


LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',  # message level to be written to console
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # this tells logger to send logging message
                                 # to its parent (will send if set to True)
        },
        'django.db': {
            # django also has database level logging
        },
    },
}
