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
from environs import Env # New 20201221

env = Env()     # New 20201221
env.read_env()  # New 20201221

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allows one Django project to control multiple sites.
    'django.contrib.sites', # New 20201221

    # Local
    'accounts', # New 20201220
    'pages',    # New 20201220
    'books',    # New 20201221

    # Third-party
    'crispy_forms',     # New 20201221
    'allauth',          # New 20201221
    'allauth.account',  # New 20201221
    'debug_toolbar',    # New 20201222
]

CRISPY_TEMPLATE_PACK = 'bootstrap4' # New 20201221

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
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
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
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
DEFAULT_FROM_EMAIL = 'jatlast@hotmail.com'    # New 20201221

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # New 20201221
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # New 20201221
EMAIL_HOST = env("EMAIL_HOST_KEY")
EMAIL_HOST_USER = env("EMAIL_HOST_USER_KEY")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD_KEY")
EMAIL_PORT = env("EMAIL_PORT_KEY")
EMAIL_USE_TLS = env("EMAIL_USE_TLS_KEY")

MEDIA_URL = '/media/'                           # New 20201222
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))    # New 20201222

# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]