from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(=&cx1&xpv@$=^saddpo!6yqzg_c1d#c5n!hq(1$na8lv27-xv'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from local_settings import *
    print "Imported local settings"
except ImportError:
    print "Failed to import local settings"
    pass
