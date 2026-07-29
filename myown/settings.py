"""
Django settings for myown project.
"""

from pathlib import Path
import os
import dj_database_url


# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent


# Security

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-key"
)


DEBUG = True


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "myown-njc8.onrender.com",
]


CSRF_TRUSTED_ORIGINS = [
    "https://myown-njc8.onrender.com",
]


# Applications

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'myapp',
]


# Middleware

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'myown.urls'


# Templates

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Added templates folder support
        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


WSGI_APPLICATION = 'myown.wsgi.application'


# Database

DATABASES = {

    "default": dj_database_url.config(

        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",

        conn_max_age=600,

        ssl_require=True

    )
}



# Password validation

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# Language and timezone

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



# Static files

STATIC_URL = '/static/'


STATIC_ROOT = BASE_DIR / 'staticfiles'


STATICFILES_DIRS = [

    BASE_DIR / 'myapp' / 'static',

]


STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Local database
# """
# Django settings for myown project.
# """

# from pathlib import Path
# import os
# import dj_database_url


# # Build paths inside the project
# BASE_DIR = Path(__file__).resolve().parent.parent


# # ======================================================
# # Security
# # ======================================================

# SECRET_KEY = os.environ.get(
#     "SECRET_KEY",
#     "django-insecure-change-this-key"
# )


# DEBUG = os.environ.get(
#     "DEBUG",
#     "True"
# ) == "True"


# ALLOWED_HOSTS = [

#     "localhost",

#     "127.0.0.1",

#     "myown-njc8.onrender.com",

# ]


# CSRF_TRUSTED_ORIGINS = [

#     "http://localhost:8000",

#     "http://127.0.0.1:8000",

#     "https://myown-njc8.onrender.com",

# ]


# # Local development
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False



# # ======================================================
# # Applications
# # ======================================================

# INSTALLED_APPS = [

#     "django.contrib.admin",

#     "django.contrib.auth",

#     "django.contrib.contenttypes",

#     "django.contrib.sessions",

#     "django.contrib.messages",

#     "django.contrib.staticfiles",


#     "myapp",

# ]



# # ======================================================
# # Middleware
# # ======================================================

# MIDDLEWARE = [

#     "django.middleware.security.SecurityMiddleware",

#     "whitenoise.middleware.WhiteNoiseMiddleware",

#     "django.contrib.sessions.middleware.SessionMiddleware",

#     "django.middleware.common.CommonMiddleware",

#     "django.middleware.csrf.CsrfViewMiddleware",

#     "django.contrib.auth.middleware.AuthenticationMiddleware",

#     "django.contrib.messages.middleware.MessageMiddleware",

#     "django.middleware.clickjacking.XFrameOptionsMiddleware",

# ]



# ROOT_URLCONF = "myown.urls"



# # ======================================================
# # Templates
# # ======================================================

# TEMPLATES = [

#     {

#         "BACKEND":
#         "django.template.backends.django.DjangoTemplates",

#         "DIRS": [],

#         "APP_DIRS": True,

#         "OPTIONS": {

#             "context_processors": [

#                 "django.template.context_processors.request",

#                 "django.contrib.auth.context_processors.auth",

#                 "django.contrib.messages.context_processors.messages",

#             ],

#         },

#     },

# ]



# WSGI_APPLICATION = "myown.wsgi.application"



# # ======================================================
# # Database
# # ======================================================

# DATABASE_URL = os.environ.get("DATABASE_URL")


# if DATABASE_URL:


#     # Render PostgreSQL

#     DATABASES = {

#         "default": dj_database_url.parse(

#             DATABASE_URL,

#             conn_max_age=600,

#             ssl_require=True,

#         )

#     }


# else:


#     # Local SQLite

#     DATABASES = {

#         "default": {

#             "ENGINE":
#             "django.db.backends.sqlite3",

#             "NAME":
#             BASE_DIR / "db.sqlite3",

#         }

#     }




# # ======================================================
# # Password Validation
# # ======================================================

# AUTH_PASSWORD_VALIDATORS = [

#     {

#         "NAME":
#         "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",

#     },

#     {

#         "NAME":
#         "django.contrib.auth.password_validation.MinimumLengthValidator",

#     },

#     {

#         "NAME":
#         "django.contrib.auth.password_validation.CommonPasswordValidator",

#     },

#     {

#         "NAME":
#         "django.contrib.auth.password_validation.NumericPasswordValidator",

#     },

# ]



# # ======================================================
# # Language / Time
# # ======================================================

# LANGUAGE_CODE = "en-us"

# TIME_ZONE = "Asia/Kolkata"

# USE_I18N = True

# USE_TZ = True



# # ======================================================
# # Static Files
# # ======================================================

# STATIC_URL = "/static/"

# STATIC_ROOT = BASE_DIR / "staticfiles"


# STATICFILES_DIRS = [

#     BASE_DIR / "myapp" / "static",

# ]


# STATICFILES_STORAGE = (
#     "whitenoise.storage.CompressedManifestStaticFilesStorage"
# )



# # ======================================================
# # Default Primary Key
# # ======================================================

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"