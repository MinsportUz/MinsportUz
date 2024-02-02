import os
from minsport.base import BASE_DIR
from decouple import config
DEBUG = config('DEBUG') == 'False'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config('PASSWORD'),
        'HOST': config("HOST"),
        'PORT': config('PORT'),
    }
}