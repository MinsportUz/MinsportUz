import os

from decouple import config
from .base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'minsport',
#         'USER': 'root',
#         'PASSWORD': 'Bo977731030#',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}