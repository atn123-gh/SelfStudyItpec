from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str('POSTGRES_NAME'),
        "USER": env.str('POSTGRES_USER'),
        "PASSWORD":env.str('POSTGRES_PASSWORD'),
        "HOST":env.str('POSTGRES_HOST'),
        "PORT": env.str('POSTGRES_PORT')
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa: F405



# CACHES
# ------------------------------------------------------------------------------
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env("REDIS_URL"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # Mimicing memcache behavior.
#             # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
#             "IGNORE_EXCEPTIONS": True,
#         },
#     }
# }

# # SECURITY
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# # https://docs.djangoproject.com/en/4.2/ref/settings/#secure-ssl-redirect
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

CSRF_COOKIE_DOMAIN= '.selfstudyitpec.com'

# CORS_ALLOWED_ORIGINS = [
#     "https://www.selfstudyitpec.com",
#     "https://www.itpec.selfstudyitpec.com",
# ]

CSRF_TRUSTED_ORIGINS = [
    "https://selfstudyitpec.com",
    "https://www.selfstudyitpec.com",
    # "https://www.itpec.selfstudyitpec.com",
    ]


# # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# # https://docs.djangoproject.com/en/4.2/ref/settings/#secure-hsts-seconds
# # TODO: set this to 60 seconds first and then to 518400 once you prove the former works
# SECURE_HSTS_SECONDS = 60
# # https://docs.djangoproject.com/en/4.2/ref/settings/#secure-hsts-include-subdomains
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# # https://docs.djangoproject.com/en/4.2/ref/settings/#secure-hsts-preload
# SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# # https://docs.djangoproject.com/en/4.2/ref/middleware/#x-content-type-options-nosniff
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# STATIC
# ------------------------
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# MEDIA
# ------------------------------------------------------------------------------

# # EMAIL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email
# DEFAULT_FROM_EMAIL = env(
#     "DJANGO_DEFAULT_FROM_EMAIL",
#     default="ITPEC Study <noreply@example.com>",
# )
# # https://docs.djangoproject.com/en/4.2/ref/settings/#server-email
# SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# # https://docs.djangoproject.com/en/4.2/ref/settings/#email-subject-prefix
# EMAIL_SUBJECT_PREFIX = env(
#     "DJANGO_EMAIL_SUBJECT_PREFIX",
#     default="[ITPEC Study] ",
# )

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
# ADMIN_URL = env("DJANGO_ADMIN_URL")

# # Anymail
# # ------------------------------------------------------------------------------
# # https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
# INSTALLED_APPS += ["anymail"]  # noqa: F405
# # https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend
# # https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# # https://anymail.readthedocs.io/en/stable/esps
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# ANYMAIL = {}


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
        # ,   
        # "file": {
        #     "level": "DEBUG",
        #     "class": "logging.FileHandler",
        #     "filename": "logs/django_log.log",  # Change this to your desired file path
        #     "formatter": "verbose",
        # }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}


# Your stuff...
# ------------------------------------------------------------------------------

BBASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

STATIC_ROOT = str(BBASE_DIR / "staticfiles") # for collectstatic #BBASE_DIR /code/


STATICFILES_DIRS = [
    BASE_DIR / "static",  #BASE_DIR /code/itp_project
]

