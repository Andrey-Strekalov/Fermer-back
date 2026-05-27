from pathlib import Path
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-dev-secret-key')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_TZ = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'apps.users',
    'apps.bids',
    'corsheaders',
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u3433347_Fermer_DB',
        'USER': 'u3433347_DB',
        'PASSWORD': 'Kcx-3aZ-iVu-9Yv',
        'HOST': 'localhost',
    }
}

WSGI_APPLICATION = 'config.wsgi.application'

# Custom user model
AUTH_USER_MODEL = 'users.User'

ROOT_URLCONF = 'config.urls'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'config.exception_handler.custom_exception_handler',
}


STATIC_URL = '/static/'
STATIC_ROOT = "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # папка под шаблоны (может не существовать)
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

CORS_ALLOW_ALL_ORIGINS = True
