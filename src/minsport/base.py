import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

# APPEND_SLASH = True

INSTALLED_APPS = [
    'modeltranslation',
    'rolepermissions',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'sorl.thumbnail',
    # API
    'rest_framework',
    # Panel
    'admin_panel',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.default_language.CustomLocaleMiddleware'
]

ROOT_URLCONF = 'minsport.urls'

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
                'django.template.context_processors.i18n',

            ],
        },
    },
]

MAX_UPLOAD_SIZE = "104857600"
DATA_UPLOAD_MAX_MEMORY_SIZE = None

WSGI_APPLICATION = 'minsport.wsgi.application'

ROLEPERMISSIONS_MODULE = 'minsport.roles'

# Image Cropping
DJANGORESIZED_DEFAULT_QUALITY = 81

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

# API hostname
HOST = 'https://backend.minsport.uz'

# FRONTEND hostname
FRONT = 'https://minsport.uz/'

# Rest framework settings

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    #     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    #     'PAGE_SIZE': None
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ALLOW_METHODS = [
    '*'
]

CORS_ALLOW_HEADERS = [
    '*'
]
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
gettext = lambda s: s
LANGUAGES = (
    ('uz', gettext('Uzbek')),
    ('en', gettext('English')),
    ('ru', gettext('Russian')),
    ('sr', gettext('Ozbek')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'en', 'ru', 'sr')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'en', 'ru', 'sr')
TRANSLATABLE_MODEL_MODULES = ['HomePage', ]
# MODELTRANSLATION_ENABLE_FALLBACKS = False

MODELTRANSLATION_TRANSLATION_FILES = (
    'admin_panel.translation.translate',
)

# Login URL
LOGIN_URL = '/panel/login/'

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

CHANNEL_ID = config('CHANNEL_ID')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
