"""
Django settings for certify project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5i7h241^@n$+6m@(psq@k+u!*^gi9vtz#d+i!oc1s*qn#d*#p@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['certify.com', '.certify.com']

# Application definition


SHARED_APPS = [
    'django_tenants',  # mandatory

    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',

    # 'services',
    # 'django_tables2',
    'tenant',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'public',
    'accounts',
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'services',
    'django_tables2',
    # 'tenant'
    'rest_framework',
    'accounts',
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "tenant.Client"  # app.Model
TENANT_DOMAIN_MODEL = "tenant.Domain"  # app.Model

ROOT_URLCONF = 'certify.urls'
PUBLIC_SCHEMA_URLCONF = 'certify.urls_public'
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
PUBLIC_SCHEMA_NAME = 'public'


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'certify.middleware.CustomAuthenticationBackend',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AUTHENTICATION_BACKENDS=['certify.middleware.CustomAuthenticationBackend',]




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # set this explicitly
                'certify.context_preprocessors.settings_export',
            ],
            'libraries': {
                'tags': 'certify.tags',
                'filters': 'certify.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'certify.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'certify3',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# manually added
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login'

MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'accounts.User'


# region CUSTOM CONSTANTS
from types import SimpleNamespace

CONTENT_TITLE = SimpleNamespace(**{
    'DASHBOARD': 'Dashboard',
    'TEMPLATES': 'Templates',
    'DATASHEETS': 'Datasheets',
    'CERTIFICATES': 'Certificates',
    'MY_CERTIFICATES': 'Certificates Awarded To Me',
    'CERTIFICATE_SETUP': 'Certificate Setup',
    'CERTIFICATE_GENERATE': 'Certificate Generate',
    'CERTIFICATE_GENERATED': 'Past Certificates',
    'EVENTS': 'Events',
    'AWARDEES': 'Awardees',
    'REPORTS': 'Reports',
})

EVENT_STATUS = SimpleNamespace(**{
    'PENDING_TEMPLATE': 'Template Pending',  # Just the name and descriptions are added
    'PENDING_DATASHEET': 'Data Sheet Pending',
    'PENDING_PAYMENT': 'Payment Pending',
    'MISMATCHING_KEYS': 'Mismatching Keys',
    'INVALID_DATA_KEYS': 'Mandatory Keys Missing',
    'READY_TO_GENERATE': 'Ready To Generate',
    'CERTIFICATE_GENERATED': 'Generated',
})
# endregion

# region CONFIGURATIONS
IS_HARDCODED_OTP = True
IS_HARDCODED_PASSWORD_GENERATED = True
DATE_FORMAT = 'M d, Y'
OUR_DISPLAY_NAME = 'Certify'
# endregion

REST_FRAMEWORK = {

}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    #     # 'rest_framework.authentication.SessionAuthentication',
    # ]
}
# APPEND_SLASH = True


# region Internationalization
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('hi', _('Hindi')),
    ('ja', _('Japanese')),
    ('ar', _('Arabic')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
# endregion
