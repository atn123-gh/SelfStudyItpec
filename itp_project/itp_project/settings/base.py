"""
Base settings to build other settings files upon.
"""
from pathlib import Path
import os

import environ
from dotenv import load_dotenv

load_dotenv()

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Optional - only enabled if SENTRY_DSN is set. No default DSN is baked in,
# so a fresh clone/deployment doesn't send error telemetry anywhere unless
# you explicitly configure it.
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production,
    profiles_sample_rate=1.0,
    )


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# itpec_study/
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/4.2/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/4.2/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('pt-br', _('Português')),
# ]
# https://docs.djangoproject.com/en/4.2/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/4.2/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": env.db(
#         "DATABASE_URL",
#         default="postgres:///itpec_study",
#     ),
# }

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# django_project/settings.py


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "itpdb",
#         "USER": "itp_user",
#         "PASSWORD": "itp_pass",
#         "HOST": "db",  # set in docker-compose.yml
#         "PORT": 5433,  # default postgres port
#     }
# }


# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#root-urlconf
# ROOT_URLCONF = "config.urls"
ROOT_URLCONF = "itp_project.urls"

# https://docs.djangoproject.com/en/4.2/ref/settings/#wsgi-application
# WSGI_APPLICATION = "config.wsgi.application"
WSGI_APPLICATION = "itp_project.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
    #  "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "webpack_loader",
]

LOCAL_APPS = [
    "home.apps.HomeConfig",
    "quiz.apps.QuizConfig",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# # MIGRATIONS
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/4.2/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "itpec_study.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#authentication-backends
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]
# # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-user-model
# AUTH_USER_MODEL = "users.User"
# # https://docs.djangoproject.com/en/4.2/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# # https://docs.djangoproject.com/en/4.2/ref/settings/#login-url
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#static-root


# https://docs.djangoproject.com/en/4.2/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/4.2/ref/settings/#dirs
        "DIRS":  [os.path.join(BASE_DIR, 'templates')], 
        # https://docs.djangoproject.com/en/4.2/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/4.2/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # "itpec_study.users.context_processors.allauth_settings",
            ],
        },
    }
]

# # https://docs.djangoproject.com/en/4.2/ref/settings/#form-renderer
# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# # FIXTURES
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/4.2/ref/settings/#fixture-dirs
# FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend
# EMAIL_BACKEND = env(
#     "DJANGO_EMAIL_BACKEND",
#     default="django.core.mail.backends.smtp.EmailBackend",
# )
# https://docs.djangoproject.com/en/4.2/ref/settings/#email-timeout
# EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/4.2/ref/settings/#admins
ADMINS = [("""author_abc""", "author_abc@example.com")]
# https://docs.djangoproject.com/en/4.2/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # "file": {
        #     "level": "DEBUG",
        #     "class": "logging.FileHandler",
        #     "filename": "logs/django_log.log",  # Change this to your desired file path
        #     "formatter": "verbose",
        # }
    },
    # "root": {"level": "INFO", "handlers": ["console","file"]},
    "root": {"level": "INFO", "handlers": ["console"]},

}


# # django-allauth
# # ------------------------------------------------------------------------------
# ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# # https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_AUTHENTICATION_METHOD = "username"
# # https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_EMAIL_REQUIRED = True
# # https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# # https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_ADAPTER = "itpec_study.users.adapters.AccountAdapter"
# # https://django-allauth.readthedocs.io/en/latest/forms.html
# ACCOUNT_FORMS = {"signup": "itpec_study.users.forms.UserSignupForm"}
# # https://django-allauth.readthedocs.io/en/latest/configuration.html
# SOCIALACCOUNT_ADAPTER = "itpec_study.users.adapters.SocialAccountAdapter"
# # https://django-allauth.readthedocs.io/en/latest/forms.html
# SOCIALACCOUNT_FORMS = {"signup": "itpec_study.users.forms.UserSocialSignupForm"}


# django-webpack-loader
# ------------------------------------------------------------------------------
# WEBPACK_LOADER = {
#     "DEFAULT": {
#         "CACHE": not DEBUG,
#         "STATS_FILE": BASE_DIR / "webpack-stats.json",
#         "POLL_INTERVAL": 0.1,
#         "IGNORE": [r".+\.hot-update.js", r".+\.map"],
#     }
# }
# Your stuff...
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/4.2/ref/settings/#static-url
STATIC_URL = "/static/"