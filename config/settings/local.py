from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'тонна-снг.рф',
    'xn----7sbk1bacc2ad.xn--p1ai'
]

SECRET_KEY = "fml**6z4!(zyw742=#sq2%7a=xa#=cd$9u&+t_e)ra5q)v#7xr"

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

CORS_ALLOW_ALL_ORIGINS = True
