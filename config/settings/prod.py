from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ".onrender.com"
]

# Render использует proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = "fml**6z4!(zyw742=#sq2%7a=xa#=cd$9u&+t_e)ra5q)v#7xr"

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS (разрешаем фронту)
CORS_ALLOW_ALL_ORIGINS = True