"""
Django settings for skymarket project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Для debug версии
BASE_DIR = Path(__file__).resolve().parent.parent
# Для сервера версии
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']



# Application definition
INSTALLED_APPS = [
    # my_app
    'redoc.apps.RedocConfig',
    'users.apps.UsersConfig',
    'ads.apps.AdsConfig',

    # Фильтры django-filter
    'django_filters',

    "corsheaders",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # приложения свое для авторизации
    # 'accounts',

    # rest API implementation library for django
    "rest_framework",

    # JWT authentication backend library
    'rest_framework_simplejwt',
    # 'rest_framework.authtoken'
    # third party package for user registration and authentication endpoints
    'djoser',

    # Other apps…
    "phonenumber_field",

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.yahoo',
    # 'allauth.socialaccount.providers.yandex',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skymarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'skymarket.wsgi.application'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
# }
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# здесь мы настраиваем Djoser
DJOSER = {
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==== ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ PostgreSQL ====
# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DB_ENGINE'),
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ru-ru'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATICFILES_DIRS = [
#     # BASE_DIR / "config/static/",
#     os.path.join(BASE_DIR, "static/"),
# ]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# """ The user is required to hand over an e-mail address when signing up. """
# ACCOUNT_EMAIL_REQUIRED = True
#
# """ Enforce uniqueness of e-mail addresses. The emailaddress.email model field is set to UNIQUE.
#  Forms prevent a user from registering with or adding an additional email address if
#  that email address is in use by another account. """
# ACCOUNT_UNIQUE_EMAIL = True
#
# """ The user is required to enter a username when signing up.
#  Note that the user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set to email.
#  Set to False when you do not wish to prompt the user to enter a username. """
# ACCOUNT_USERNAME_REQUIRED = False
#
# """ (=”username” | “email” | “username_email”)
#     Specifies the login method to use – whether the user logs in by entering their username,
#     e-mail address, or either one of both. Setting this to “email” requires ACCOUNT_EMAIL_REQUIRED=True """
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
#
# """ Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none". """
# ACCOUNT_EMAIL_VERIFICATION = True
#
# ACCOUNT_FORMS = {'signup': 'accounts.forms.MyCustomSignupForm'}
# SOCIALACCOUNT_FORMS = {'signup': 'accounts.forms.MyCustomSocialSignupForm'}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Настройки электронной почты
EMAIL_HOST = os.environ.get('HOST_SMTP_YA')
EMAIL_PORT = os.environ.get('PORT_SMTP')

EMAIL_HOST_USER = os.environ.get('HOST_USER_YA')  # ваш QQ Номер счета и код авторизации
EMAIL_HOST_PASSWORD = os.environ.get('YANDEX_ID')
EMAIL_USE_TLS = True  # Здесь должно быть True, Иначе отправка не удалась

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True

# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'yandex': {
#         'APP': {
#             'client_id': os.environ.get('YA_ID'),
#             'secret': os.environ.get('YA_PA'),
#             'key': '',
#         }
#     },
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': os.environ.get('APP_CLIENT_ID'),
#             'secret': os.environ.get('APP_SECRET'),
#             'key': '',
#         }
#     }
# }
