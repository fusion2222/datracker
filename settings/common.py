import os
import json

# Open config file and read project ENV variables.
with open('env.json') as f:
    CONFIG = json.loads(f.read())

DJANGO_CONFIGURATION = CONFIG.get('DJANGO_CONFIGURATION', 'Prod')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('SECRET_KEY', 'dev-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('DEBUG', False)

ALLOWED_HOSTS = []

SITE_HOST = CONFIG.get('SITE_HOST', 'localhost:8000')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'djsingleton',
    'datracker',
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

ROOT_URLCONF = 'datracker.urls'

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
                'datracker.context_processors.navbar_menu',
            ],
        },
    },
]

STATIC_URL = '/static/'

STATICFILE_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder'
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

AUTH_USER_MODEL = 'datracker.Employee'

STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', os.path.join(BASE_DIR, 'static_root'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.environ.get('DJANGO_STATIC_ROOT', os.path.join(BASE_DIR, 'media_root'))

WSGI_APPLICATION = 'datracker.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

if DJANGO_CONFIGURATION != 'Dev':
    AUTH_PASSWORD_VALIDATORS += [
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
