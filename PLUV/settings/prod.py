from .base import *

if not DEBUG:
    CSRF_COOKIE_SECURE = (
        True  # to avoid transmitting the CSRF cookie over HTTP accidentally.
    )
    SESSION_COOKIE_SECURE = (
        True  # to avoid transmitting the session cookie over HTTP accidentally.
    )
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "origin"

    SESSION_COOKIE_SAMESITE = None
    CSRF_COOKIE_SAMESITE = None
    SESSION_SAVE_EVERY_REQUEST = True

    CSP_DEFAULT_SRC = ("'none'",)
    CSP_STYLE_SRC = (
        "'self'",
        "unsafe-inline" "fonts.googleapis.com",
        "'sha256-/3kWSXHts8LrwfemLzY9W0tOv5I4eLIhrf0pT8cU0WI='",
    )
    CSP_SCRIPT_SRC = ("'self'", "www.googletagmanager.com", "www.google-analytics.com")
    CSP_IMG_SRC = (
        "'self'",
        "https:",
        os.environ.get("BUCKET_SOURCE"),
        "data:",
        "www.google-analytics.com",
    )
    CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")
    CSP_CONNECT_SRC = ("'self'",)
    CSP_OBJECT_SRC = ("'none'",)
    CSP_BASE_URI = ("'none'",)
    CSP_FRAME_ANCESTORS = ("'self'", "www.youtube.com/")
    CSP_FORM_ACTION = ("'self'",)
    CSP_INCLUDE_NONCE_IN = ("script-src", "style-src")

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
    AWS_S3_SIGNATURE_VERSION = os.environ.get("AWS_SIGNATURE_VERSION", "s3v4")

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            }
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
            },
            "console_debug_false": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "logging.StreamHandler",
            },
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "console_debug_false", "mail_admins"],
                "level": "INFO",
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    # import django_heroku
    # django_heroku.settings(locals())

