"""
Django settings for tribune project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""


from __future__ import absolute_import, unicode_literals
from decouple import config
import os

DEBUG = config('DEBUG', cast=bool)


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'tribune',
    'home',
    'search',
    'images',
    'blog',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.settings',
    'wagtail.contrib.table_block',
    'wagtail.contrib.modeladmin',

    'modelcluster',
    'taggit',
    'compressor',
    'storages',
    'wagtailmenus',
    'wagtailmedia',
    'sass_processor',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'tribune.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

WSGI_APPLICATION = 'tribune.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME', default='tribune_db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'tribune', 'static'),
]
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(PROJECT_DIR, 'tribune', 'static'),
        ('node_modules', os.path.join(PROJECT_DIR, 'node_modules'))
    ]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Wagtail settings

TAGGIT_CASE_INSENSITIVE = True
TAG_SPACES_ALLOWED = True

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = config('BASE_URL')

# Wagtail settings

WAGTAIL_SITE_NAME = config('SITE_NAME', default="Tribune")

WAGTAILIMAGES_IMAGE_MODEL = 'images.CustomImage'


STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

SECRET_KEY = config('SECRET_KEY')

# Use local storage (default) for static/media instead of AWS
STORAGE_DEBUG = config('STORAGE_DEBUG', cast=bool, default=True)
if STORAGE_DEBUG:
    # Use local static files in development
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
else:
    # AWS
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).

    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

EMAIL_DEBUG = config('EMAIL_DEBUG', cast=bool, default=True)
if EMAIL_DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)

if DEBUG:
    # DEVELOPMENT
    pass
    # STATICFILES_DIRS += \
    #     ('node_modules', os.path.join(PROJECT_DIR, 'node_modules'))
else:
    # PRODUCTION
    # Allow all host headers
    ALLOWED_HOSTS = ['*']

PRODUCTION = config('PRODUCTION', cast=bool, default=False)
if PRODUCTION:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Django-sass-processor settings
SASS_PROCESSOR_ROOT = STATIC_ROOT
SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(PROJECT_DIR, 'node_modules'),
    os.path.join(PROJECT_DIR, 'extra-styles/scss'),
]
SASS_PRECISION = 8
NODE_MODULES_URL = os.path.join(STATIC_URL, 'node_modules')
SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.sass$'
