from django.contrib.messages import constants as messages  # NumericPasswordValidator
from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zzpbp5x09_cq3qz6mg)_-bj0p&z@iw%!6)-@0xmv=6tz)4+xf$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages.apps.PagesConfig",  # new
    "category.apps.CategoryConfig",  # new
    "accounts.apps.AccountsConfig",  # new
    "store.apps.StoreConfig",  # new
    "carts.apps.CartsConfig",  # new
    "orders.apps.OrdersConfig",  # new
    "axes",
    "appointment.apps.AppointmentConfig",  # new
    "supplier.apps.SupplierConfig",  # new
    "feedback",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "digitalart.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "digitalart.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#   "default": {
#       "ENGINE": "django.db.backends.sqlite3",
#       "NAME": BASE_DIR / "db.sqlite3",
#   }
# }
# DATABASES = {
#   "default": dj_database_url.config(
# Replace this value with your local database's connection string.
#       default="postgresql://postgres:postgres@localhost:5432/mysite",
#       conn_max_age=600,
#   )
# }
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_I10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
MEDIA_URL = "media/"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "static/media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_PORT = 0
EMAIL_USE_TLS = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

# Custom user model
AUTH_USER_MODEL = "accounts.Account"  # new

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    "axes.backends.AxesStandaloneBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

# Axes configuration
AXES_FAILURE_LIMIT = (
    10  # Number of login attempts before a record is created for a user's failed logins
)
AXES_LOCK_OUT_AT_FAILURE = (
    False  # Whether to lock out after `AXES_FAILURE_LIMIT` attempts
)
AXES_COOLOFF_TIME = (
    1  # Number of seconds to wait before resetting failed login attempts count
)
AXES_VERBOSE = True  # Whether to output warnings to the logger


SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True  # new
SESSION_TIMEOUT_REDIRECT = "accounts/login"  # new


# Messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.SUCCESS: "success",
    messages.INFO: "info",
}

FEEDBACK_CHOICES = (
    ("service_delivery", "Service Delivery"),
    ("product_delivery", "Product Delivery"),
)
ALLOW_ANONYMOUS_FEEDBACK = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
