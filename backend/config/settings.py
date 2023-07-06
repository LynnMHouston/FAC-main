"""
Django settings for The FAC Django backend project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from base64 import b64decode
import os
import sys
import logging
import json
import environs
from cfenv import AppEnv

import newrelic.agent

newrelic.agent.initialize()

env = environs.Env()

ENVIRONMENT = env.str("ENV", "UNDEFINED").upper()

key_service = AppEnv().get_service(name="fac-key-service")
if key_service and key_service.credentials:
    secret = key_service.credentials.get
else:
    secret = os.environ.get

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environs.Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret("SECRET_KEY")

ALLOWED_HOSTS = env("ALLOWED_HOSTS", "0.0.0.0 127.0.0.1 localhost").split()

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "local_debug_logger": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "prod_logger": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "formatter": "json",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["local_debug_logger", "prod_logger"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {"handlers": ["local_debug_logger", "prod_logger"]},
    },
}
# this shold reduce the volume of message displayed when running tests
if len(sys.argv) > 1 and sys.argv[1] == "test":
    logging.disable(logging.ERROR)


# Django application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third-party apps
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "storages",
    "djangooidc",
]

# Our apps
INSTALLED_APPS += [
    "audit",
    "api",
    "users",
    "report_submission",
    "cms",
    "data_distro",
    "dissemination",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # '/var/www/static/',
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS base
CORS_ALLOWED_ORIGINS = [env.str("DJANGO_BASE_URL", "http://localhost:8000")]

STATIC_URL = "/static/"

# Environment specific configurations
DEBUG = False
if ENVIRONMENT not in ["DEVELOPMENT", "STAGING", "PRODUCTION"]:
    # Local environment and Testing environment (CI/CD/GitHub Actions)

    if ENVIRONMENT == "LOCAL":
        DEBUG = env.bool("DJANGO_DEBUG", default=True)
    else:
        DEBUG = env.bool("DJANGO_DEBUG", default=False)

    CORS_ALLOWED_ORIGINS += ["http://0.0.0.0:8000", "http://127.0.0.1:8000"]

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
    DEFAULT_FILE_STORAGE = "report_submission.storages.S3PrivateStorage"

    # Private bucket
    AWS_PRIVATE_STORAGE_BUCKET_NAME = "gsa-fac-private-s3"
    AWS_S3_PRIVATE_REGION_NAME = os.environ.get(
        "AWS_S3_PRIVATE_REGION_NAME", "us-east-1"
    )

    # MinIO only matters for local development and GitHub action environments.
    # These should match what we're setting in backend/run.sh
    AWS_PRIVATE_ACCESS_KEY_ID = os.environ.get("AWS_PRIVATE_ACCESS_KEY_ID", "longtest")
    AWS_PRIVATE_SECRET_ACCESS_KEY = os.environ.get(
        "AWS_PRIVATE_SECRET_ACCESS_KEY", "longtest"
    )
    AWS_S3_PRIVATE_ENDPOINT = os.environ.get(
        "AWS_S3_PRIVATE_ENDPOINT", "http://minio:9000"
    )

    AWS_S3_ENDPOINT_URL = AWS_S3_PRIVATE_ENDPOINT

    DISABLE_AUTH = env.bool("DISABLE_AUTH", default=False)

else:
    # One of the Cloud.gov environments
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3ManifestStaticStorage"
    DEFAULT_FILE_STORAGE = "report_submission.storages.S3PrivateStorage"
    vcap = json.loads(env.str("VCAP_SERVICES"))
    for service in vcap["s3"]:
        if service["instance_name"] == "fac-public-s3":
            # Public AWS S3 bucket for the app
            s3_creds = service["credentials"]

            AWS_ACCESS_KEY_ID = s3_creds["access_key_id"]
            AWS_SECRET_ACCESS_KEY = s3_creds["secret_access_key"]
            AWS_STORAGE_BUCKET_NAME = s3_creds["bucket"]

            AWS_S3_REGION_NAME = s3_creds["region"]
            AWS_DEFAULT_REGION = s3_creds["region"]

            AWS_S3_CUSTOM_DOMAIN = (
                f"{AWS_STORAGE_BUCKET_NAME}.s3-{AWS_S3_REGION_NAME}.amazonaws.com"
            )
            AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

            AWS_LOCATION = "static"
            AWS_QUERYSTRING_AUTH = False
            AWS_DEFAULT_ACL = "public-read"
            STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

            STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
            AWS_IS_GZIPPED = True

        elif service["instance_name"] == "fac-private-s3":
            # Private AWS S3 bucket for the app's Excel (or other file) uploads
            s3_creds = service["credentials"]

            AWS_PRIVATE_ACCESS_KEY_ID = s3_creds["access_key_id"]
            AWS_PRIVATE_SECRET_ACCESS_KEY = s3_creds["secret_access_key"]
            AWS_PRIVATE_STORAGE_BUCKET_NAME = s3_creds["bucket"]

            AWS_S3_PRIVATE_REGION_NAME = s3_creds["region"]
            AWS_S3_PRIVATE_CUSTOM_DOMAIN = f"{AWS_PRIVATE_STORAGE_BUCKET_NAME}.s3-{AWS_S3_PRIVATE_REGION_NAME}.amazonaws.com"
            AWS_S3_PRIVATE_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

            AWS_S3_PRIVATE_ENDPOINT = s3_creds["endpoint"]
            AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_PRIVATE_ENDPOINT}"

            AWS_PRIVATE_LOCATION = "static"
            AWS_PRIVATE_DEFAULT_ACL = "private"
            # If wrong, https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl

            MEDIA_URL = (
                f"https://{AWS_S3_PRIVATE_CUSTOM_DOMAIN}/{AWS_PRIVATE_LOCATION}/"
            )

    # secure headers
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")
    # see settings options https://django-csp.readthedocs.io/en/latest/configuration.html#configuration-chapter
    bucket = f"{STATIC_URL}"
    allowed_sources = (
        "'self'",
        bucket,
        "https://idp.int.identitysandbox.gov/",
        "https://dap.digitalgov.gov",
        "https://www.google-analytics.com",
        "https://www.googletagmanager.com/",
    )
    CSP_DEFAULT_SRC = allowed_sources
    CSP_DATA_SRC = allowed_sources
    CSP_SCRIPT_SRC = allowed_sources
    CSP_CONNECT_SRC = allowed_sources
    CSP_IMG_SRC = allowed_sources
    CSP_MEDIA_SRC = allowed_sources
    CSP_FRAME_SRC = allowed_sources
    CSP_FONT_SRC = ("'self'", bucket)
    CSP_WORKER_SRC = allowed_sources
    CSP_FRAME_ANCESTORS = allowed_sources
    CSP_STYLE_SRC = allowed_sources
    CSP_INCLUDE_NONCE_IN = ["script-src"]
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    X_FRAME_OPTIONS = "DENY"

    CORS_ALLOWED_ORIGINS = [
        f"https://{AWS_S3_CUSTOM_DOMAIN}",
        env.str("DJANGO_BASE_URL"),
    ]
    CORS_ALLOW_METHODS = ["GET", "OPTIONS"]

    for service in vcap["aws-rds"]:
        if service["instance_name"] == "fac-db":
            rds_creds = service["credentials"]

    # used for psycopg2 cursor connection
    CONNECTION_STRING = (
        "dbname='{}' user='{}' port='{}' host='{}' password='{}'".format(
            rds_creds["db_name"],
            rds_creds["username"],
            rds_creds["port"],
            rds_creds["host"],
            rds_creds["password"],
        )
    )
    # Will not be enabled in cloud environments
    DISABLE_AUTH = False

# Remove once all Census data has been migrated
# Add these as env vars, look at the bucket for values
AWS_CENSUS_ACCESS_KEY_ID = secret("AWS_CENSUS_ACCESS_KEY_ID", "")
AWS_CENSUS_SECRET_ACCESS_KEY = secret("AWS_CENSUS_SECRET_ACCESS_KEY", "")
AWS_CENSUS_STORAGE_BUCKET_NAME = secret("AWS_CENSUS_STORAGE_BUCKET_NAME", "")
AWS_S3_CENSUS_REGION_NAME = secret("AWS_S3_CENSUS_REGION_NAME", "")


ADMIN_URL = "admin/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST FRAMEWORK
API_VERSION = "0"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
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

# SAM.gov API
SAM_API_URL = "https://api.sam.gov/entity-information/v3/entities"
SAM_API_KEY = secret("SAM_API_KEY")

# Data/schema directories
DATA_FIXTURES = BASE_DIR / "data_fixtures"
AUDIT_TEST_DATA_ENTRY_DIR = DATA_FIXTURES / "audit" / "test_data_entries"
AUDIT_SCHEMA_DIR = BASE_DIR / "schemas" / "output" / "audit"
SECTION_SCHEMA_DIR = BASE_DIR / "schemas" / "output" / "sections"
XLSX_TEMPLATE_JSON_DIR = BASE_DIR / "schemas" / "output" / "excel" / "json"
XLSX_TEMPLATE_SHEET_DIR = BASE_DIR / "schemas" / "output" / "excel" / "xlsx"

AV_SCAN_URL = env.str("AV_SCAN_URL", "")
AV_SCAN_MAX_ATTEMPTS = 10

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "users.auth.FACAuthenticationBackend",
]

env_base_url = env.str("DJANGO_BASE_URL", "")
secret_login_key = b64decode(secret("DJANGO_SECRET_LOGIN_KEY", ""))

# which provider to use if multiple are available
# (code does not currently support user selection)
OIDC_ACTIVE_PROVIDER = "login.gov"

OIDC_PROVIDERS = {
    "login.gov": {
        "srv_discovery_url": "https://idp.int.identitysandbox.gov",
        "behaviour": {
            # the 'code' workflow requires direct connectivity from us to Login.gov
            "response_type": "code",
            "scope": ["email", "profile:name", "phone", "all_emails"],
            "user_info_request": [
                "email",
                "first_name",
                "last_name",
                "phone",
                "all_emails",
            ],
            "acr_value": "http://idmanagement.gov/ns/assurance/ial/1",
        },
        "client_registration": {
            "client_id": "urn:gov:gsa:openidconnect.profiles:sp:sso:gsa:gsa-fac-pk-jwt-01",
            "redirect_uris": [f"{env_base_url}/openid/callback/login/"],
            "post_logout_redirect_uris": [f"{env_base_url}/openid/callback/logout/"],
            "token_endpoint_auth_method": ["private_key_jwt"],
            "sp_private_key": secret_login_key,
        },
    }
}

LOGIN_URL = f"{env_base_url}/openid/login/"

USER_PROMOTION_COMMANDS_ENABLED = ENVIRONMENT in ["LOCAL", "TESTING", "UNDEFINED"]


if DISABLE_AUTH:
    TEST_USERNAME = "test_user@test.test"
    MIDDLEWARE.append(
        "users.middleware.authenticate_test_user",
    )

    AUTHENTICATION_BACKENDS = [
        "users.auth.FACTestAuthenticationBackend",
    ]
