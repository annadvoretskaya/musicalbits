"""
Django settings for musicalbits project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ey1+2m2p770aboxc7(m=xcb4j)4cfmvzr09ow(o51dd-+-wxk='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

SOCIAL_AUTH_FACEBOOK_KEY = '1432920113671735'
SOCIAL_AUTH_FACEBOOK_SECRET = '6d16412f1d566380beb0567c2af23d57'
SOCIAL_AUTH_TWITTER_KEY = 'MG9dG1uez9qA0zjs8eq9Me3nZ'
SOCIAL_AUTH_TWITTER_SECRET = 'FPaz1XRFwhqMZoqrMTgSOG9cFlt6j3wVd3w9UMVtrbdODTmZez'
SOCIAL_AUTH_VK_OAUTH2_KEY = '4852525'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'FgU0zXnptaq0g9EPYNkC'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'main',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'musicalbits.urls'

WSGI_APPLICATION = 'musicalbits.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbmusic',
        'USER': 'root',
        'PASSWORD': 'Ann1123032z',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)