import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '&t9*(&(9*%1fzgm0)7k&@2s+xcv#+kxp2(d=8+eyojkw&lsrk1'

DEBUG = True

ENVTYPE = "LOCAL"

ALLOWED_HOSTS = ["moveti-169514.appspot.com", "localhost"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'google_handle',
    'photos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myphotos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

#WSGI_APPLICATION = 'myphotos.wsgi.application'

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    ENVTYPE = "GOOGLE"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/moveti-169514:us-central1:myphotosqlinstance',
            'NAME': 'myphoto',
            'USER': 'myphotouser',
            'PASSWORD': 'KIwyezC8F7qowzgu',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'myphoto',
            'USER': 'myphotouser',
            'PASSWORD': 'KIwyezC8F7qowzgu',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'static'
STATIC_URL = '/static/'


GOOGLE_CLOUD_STORAGE_BUCKET = 'moveti-169514.appspot.com'
GOOGLE_CLOUD_STORAGE_URL = 'http://storage.googleapis.com/bucket'
GOOGLE_CLOUD_STORAGE_DEFAULT_CACHE_CONTROL = 'public, max-age: 7200'

DEFAULT_FILE_STORAGE = 'google_handle.storage.handle.GoogleCloudStorage'
