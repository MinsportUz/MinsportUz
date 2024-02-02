from decouple import config
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'backend.minsport.uz', 'minsport.uz']
# ALLOWED_HOSTS = ['*']
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