"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""

import os

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY


DEBUG_MODE = False

# Auto-set debug mode based on App Engine dev environ
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

# Set secret keys for CSRF protection
SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_KEY = SESSION_KEY

CSRF_ENABLED = True

# Flask-DebugToolbar settings
DEBUG_TB_PROFILER_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Flask-Cache settings
CACHE_TYPE = 'gaememcached'

GOOGLE_API_CLIENT_ID = '249554462685-6poc4csf69b43rc9clumd7m791n94km5.apps.googleusercontent.com'
GOOGLE_API_CLIENT_SECRET = '_V0JuEPieBala_z5hizh8DAB'
GOOGLE_API_SCOPE = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
GOOGLE_OAUTH2_URL = 'https://accounts.google.com/o/oauth2/auth?'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_API_URL = 'https://www.googleapis.com/oauth2/v1/'
