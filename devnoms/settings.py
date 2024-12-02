from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DEVELOPMENT = 'live'
# DEVELOPMENT = "local"
DEBUG = True


if DEVELOPMENT == "local":
    # Development
    DEBUG = True
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "devnoms_localdb",
            "USER": os.getenv("DB_USER_LOCAL"),
            "PASSWORD": os.getenv("DB_PASS_LOCAL"),
            "HOST": os.getenv("DB_HOST_LOCAL"),
            "PORT": "",
        }
    }
    SITE_URL = "http://localhost:8000"


else:
    # Live
    # DEBUG = False
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME_LIVE"),
            "USER": os.getenv("DB_USER_LIVE"),
            "PASSWORD": os.getenv("DB_PASS_LIVE"),
            "HOST": os.getenv("DB_HOST_LIVE"),
            "PORT": "",
            "OPTIONS": {
                "sslmode": "require",
            },
        }
    }
    SITE_URL = "https://devnoms.onrender.com"


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chat",
    "corsheaders",
]
ASGI_APPLICATION = "devnoms.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "devnoms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "devnoms.wsgi.application"

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


LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "login"


STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "https://devnoms.onrender.com",
    "https://django-chat-application.onrender.com",
]
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "https://devnoms.onrender.com",
    "https://django-chat-application.onrender.com",
]
