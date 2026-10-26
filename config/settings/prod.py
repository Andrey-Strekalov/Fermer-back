from .base import *  # noqa: F401,F403
import os

DEBUG = False

# Static files
# STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS — только явный whitelist в продакшне
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL", "redis://localhost:6379/0")],
        },
    }
}
