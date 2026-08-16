from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key
# Required, no fallback - set DJANGO_SECRET_KEY in .env (see .env.example).
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
ALLOWED_HOSTS += env.list("DJANGO_ALLOWED_HOSTS", default=[])
# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites

# INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
# DEBUG_TOOLBAR_CONFIG = {
#     "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
#     "SHOW_TEMPLATE_CONTEXT": True,
# }
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
# INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

print("LOCAL SETTING ########################")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "itpdb",
#         "USER": "itp_user",     
#         "PASSWORD": "itp_pass",
#         'PORT': '5432'
#     }
# }
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



from urllib.parse import quote_plus

MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'mongo_db')
MONGO_DB_HOST = os.getenv('MONGO_DB_HOST', 'mongodb://mongodb:27017')
MONGO_DB_USERNAME = quote_plus(os.getenv('MONGO_DB_USERNAME', 'root'))
MONGO_DB_PASSWORD = quote_plus(os.getenv('MONGO_DB_PASSWORD', 'example'))

# Remove mongodb:// prefix if present
MONGO_DB_HOST = MONGO_DB_HOST.replace('mongodb://', '')

MONGO_URI = f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}"



STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

BBASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
STATIC_ROOT = str(BBASE_DIR / "staticfiles") # for collectstatic #BBASE_DIR /code/
