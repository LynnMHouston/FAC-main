"""
Django settings for The FAC Django backend project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import json
import environs
from cfenv import AppEnv

env = environs.Env()
environment = env.str("ENV", "UNDEFINED").upper()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environs.Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-(jdhaxma6e-)uq=!a0*&z%#b_3-d#wnq0w51#^***5u%@z6thh",
)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {"json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"}},
    "handlers": {
        "local_debug_logger": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "prod_logger": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "formatter": "json",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {"django": {"handlers": ["local_debug_logger", "prod_logger"]}},
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "report_submission",
    "cms",
]

# Third-party apps

INSTALLED_APPS += ["rest_framework", "rest_framework.authtoken", "corsheaders"]

# Our apps

INSTALLED_APPS += ["audit", "api", "users"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL", default="postgres://postgres:password@0.0.0.0/backend"
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_ROOT = str(BASE_DIR.joinpath("static"))
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # '/var/www/static/',
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

# Environment specific configurations
if environment == "TESTING":
    return
elif environment != "LOCAL":
    vcap = json.loads(env.str("VCAP_SERVICES"))
    for service in vcap["s3"]:
        # need to confirm the name of the bucket and that it is public
        if service["instance_name"] == "fac_dev_s3":
            # Public AWS S3 bucket for the app
            s3_creds = service["credentials"]

    AWS_STORAGE_BUCKET_NAME = s3_creds["bucket"]
    AWS_S3_REGION_NAME = s3_creds["region"]
    AWS_S3_CUSTOM_DOMAIN = (
        f"{AWS_STORAGE_BUCKET_NAME}.s3-{AWS_S3_REGION_NAME}.amazonaws.com"
    )
    AWS_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
else:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = env.bool("DJANGO_DEBUG", default=False)

ADMIN_URL = "admin/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Whitenoise for serving static files -- Just the admin interface
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# REST FRAMEWORK
API_VERSION = "0"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "users.auth.ExpiringTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "api",
}

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "AUDIENCE": None,
    "ISSUER": "https://idp.int.identitysandbox.gov/",
    "JWK_URL": "https://idp.int.identitysandbox.gov/api/openid_connect/certs",
    "LEEWAY": 0,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.UntypedToken",),
    "USER_ID_CLAIM": "sub",
}

TOKEN_AUTH = {"TOKEN_TTL": 3600}

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# SAM.gov API
SAM_API_URL = "https://api.sam.gov/entity-information/v3/entities"
# Get key from cloud.gov user provided service instance
env = AppEnv()
key_service = env.get_service(name="fac-key-service")
if key_service and key_service.credentials:
    SAM_API_KEY = key_service.credentials.get("SAM_API_KEY")
else:
    SAM_API_KEY = os.environ.get("SAM_API_KEY")

SCHEMAS_DIR = os.path.join("audit", "schemas")
SECTION_SCHEMA_DIR = os.path.join("schemas", "sections")
