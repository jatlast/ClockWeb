"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
# FYI: After creating a new application in Django with "startapp"
#   ones still needs to configure: the model, view, url, and template for each page 
from pathlib import Path

# from environs import Env # New 20201221

# env = Env()     # New 20201221
# env.read_env()  # New 20201221

import environ # New 20210103
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# For demo purposes only (not working)
#from pprint import pprint
#pprint(env.dump(), indent=2)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)
#DEBUG = True

ALLOWED_HOSTS = ['miclockrepair.com', 'localhost','127.0.0.1', '10.16.0.114', '10.16.0.110']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
#    'whitenoise.runserver_nostatic', # New 20201222
    'django.contrib.staticfiles',

    # allows one Django project to control multiple sites.
    'django.contrib.sites', # New 20201221
    # GeoDjango for location aware web applications
    'django.contrib.gis',   # New 20210101
    # number formatting in templates
    'django.contrib.humanize', # New 20210103

    # Local
    'accounts', # New 20201220
    'pages',    # New 20201220
#    'books',   # New 20201221 | Removed 20201228
    'customer', # New 20201223
    'clocktype',# New 20201224
    'clock',    # New 20201224
    'repairer', # New 20201231

    # Third-party
    'crispy_forms',     # New 20201221
    'allauth',          # New 20201221
    'allauth.account',  # New 20201221
    'debug_toolbar',    # New 20201222
#    'phone_field',     # New 20201223
    'phonenumber_field',# New 20201223
    # HTML GEO Location only works in https mode
    'sslserver',        # New 20210101
    # for better map displays in HTML
    'floppyforms',      # New 20210101
]

CRISPY_TEMPLATE_PACK = 'bootstrap4' # New 20201221
#PHONENUMBER_DB_FORMAT = 'NATIONAL' # New 20201223
PHONENUMBER_DEFAULT_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'US'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
#    'whitenoise.middleware.WhiteNoiseMiddleware', # New 20201222
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))], # New 20201220
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str("POSTGRES_DB", default='postgres'),
        'USER': env.str("POSTGRES_USER", default='postgres'),
        'PASSWORD': env.str("POSTGRES_PASS", default='postgres'),
        'HOST': 'db',
        'PORT': 5432
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Detroit'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# django-allauth config             # New 20201221
LOGIN_REDIRECT_URL = 'home'         # New 20201220
ACCOUNT_LOGOUT_REDIRECT = 'home'    # New 20201221
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)                                   # New 20201221
ACCOUNT_SESSION_REMEMBER = True     # New 20201221
# Disable the second password field in the signup form (django-allauth facilitates easy password changes)...
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False # New 20201221

# config django-allauth to use unique email address as username  
ACCOUNT_USERNAME_REQUIRED = False       # New 20201221
ACCOUNT_AUTHENTICATION_METHOD = 'email' # New 20201221
ACCOUNT_EMAIL_REQUIRED = True           # New 20201221
ACCOUNT_UNIQUE_EMAIL = True             # New 20201221

AUTH_USER_MODEL = 'accounts.CustomUser' # New 20201220

#DEFAULT_FROM_EMAIL = 'admin@djangobookstore.com'    # New 20201221
DEFAULT_FROM_EMAIL = 'admin@miclockrepair.com'    # New 20201221

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # New 20201221
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # New 20201221
#EMAIL_HOST = env("EMAIL_HOST_KEY", default="miclockrepair-com.mail.protection.outlook.com")
#EMAIL_HOST_USER = env("EMAIL_HOST_USER_KEY", default="admin@miclockrepair.com")
EMAIL_HOST = env("EMAIL_HOST_KEY", default="smtpout.secureserver.net")
EMAIL_HOST_USER = env("EMAIL_HOST_USER_KEY", default="admin@miclockrepair.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD_KEY", default="PhnomPenh0")
#EMAIL_PORT = env("EMAIL_PORT_KEY", default="586")
#EMAIL_USE_SSL = env("EMAIL_USE_SSL_KEY", default="True")
#EMAIL_USE_TLS = env("EMAIL_USE_TLS_KEY", default="False")
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

MEDIA_URL = '/media/'                           # New 20201222
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))    # New 20201222

# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
