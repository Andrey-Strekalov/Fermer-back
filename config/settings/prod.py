from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'тонна-снг.рф',
    'xn----7sbk1bacc2ad.xn--p1ai'
]

# Render использует proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = "fml**6z4!(zyw742=#sq2%7a=xa#=cd$9u&+t_e)ra5q)v#7xr"

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS (разрешаем фронту)
CORS_ALLOW_ALL_ORIGINS = True