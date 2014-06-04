"""
Django settings for CVM project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from unipath import Path

BASE_DIR = Path(__file__).ancestor(2)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aoumvt^i@d%_2m99)$$&mc=h6egs!il(8jd8rt5kx&jgj!!i*q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS =(
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS=(
    'south',
    'mptt',
    'django_extensions',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'debug_toolbar',

)
LOCAL_APPS=(
    'apps.adscripciones',
    'apps.elementos',
)


INSTALLED_APPS =THIRD_PARTY_APPS + DJANGO_APPS  + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'CVM.urls'

WSGI_APPLICATION = 'CVM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cvmdb',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'alfonso',
        'PASSWORD': '123',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS=(BASE_DIR.child('public').child('static'),)

#***Estas lineas es para que funcione con VAGRANT
if DEBUG:
    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt): return True
            return False

    INTERNAL_IPS = glob_list(['127.0.0.1', '192.168.*.*'])