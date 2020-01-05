from .base import *  # NOQA

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zhangblogidea_db',
        'USER': 'root',
        'PASSWORD': 'python',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}
