from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ".onrender.com"
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Render использует proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECRET_KEY = os.environ.get("SECRET_KEY")

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS (разрешаем фронту)
CORS_ALLOW_ALL_ORIGINS = True