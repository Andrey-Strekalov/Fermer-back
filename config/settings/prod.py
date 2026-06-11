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

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS (разрешаем фронту)
CORS_ALLOW_ALL_ORIGINS = True

# pip install channels-redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(os.getenv('REDIS_HOST', '127.0.0.1'), int(os.getenv('REDIS_PORT', '6379')))]},
    }
}