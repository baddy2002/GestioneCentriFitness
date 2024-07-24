import sys
import dj_database_url
from os import getenv, path
from pathlib import Path
import dotenv 
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Environment variables file
dotenv_file = BASE_DIR / '.env.local'

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEVELOPMENT_MODE = getenv("DEVELOPMENT_MODE", "False") == "True"                    #Dev or prod

SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())                   #application key 

DEBUG = getenv("DEBUG", 'False') == 'True'                                          #debug mode(for errors)

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOST", "127.0.0.1,localhost").split(",")     #allowed host list(in prod will be the address of the fe microservice)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',                              #cors per next js
    'centerHandling',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',                #cors per next js
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FitnessCenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FitnessCenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'GestioneCentriFitness_CenterHandling',
            'USER': 'postgres',
            'PASSWORD': 'password123',
            'HOST': 'localhost',
            'PORT': '5959'
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if getenv("DATABASE_URL", None) is None:                                                #DATABASE_URL DA CAMBIARE PER PROFILO PROD
        raise Exception("Database URL is not defined!")
    DATABASES = {
        'default': dj_database_url.parse(getenv('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#static and media url 
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS=getenv('GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS')
if DEVELOPMENT_MODE is True:
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    GS_BUCKET_NAME = 'your-google-cloud-storage-bucket-name'
    GS_DEFAULT_ACL = 'publicRead'
    GS_OBJECT_PARAMETERS = {
        'cache_control': 'max-age=86400'
    }
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
            },
        },
    }
    
    STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
    
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
CORS_ALLOW_CREDENTIALS = True                                                                                                  #Cors host security(only frontend or others backend microservices should be in the list)

#Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

APPEND_SLASH=False      #per non aggiungere automaticamente slash in richieste post(nei template auto gestito)

if DEVELOPMENT_MODE:
    BACKEND_SERVICE_PROTOCOL='http'
    BACKEND_SERVICE_DOMAIN='127.0.0.1'
    BACKEND_SERVICE_PORT=8001
    BACKEND_SSO_SERVICE_PROTOCOL='http'
    BACKEND_SSO_SERVICE_DOMAIN='127.0.0.1'
    BACKEND_SSO_SERVICE_PORT=8000
else:
    BACKEND_SSO_SERVICE_PROTOCOL=getenv('BACKEND_SSO_SERVICE_PROTOCOL', 'http')
    BACKEND_SSO_SERVICE_DOMAIN=getenv('BACKEND_SSO_SERVICE_DOMAIN','http://127.0.0.1')
    BACKEND_SSO_SERVICE_PORT=getenv('BACKEND_SSO_SERVICE_PORT', 8000)
    BACKEND_SERVICE_PROTOCOL=getenv('BACKEND_SERVICE_PROTOCOL', 'http')
    BACKEND_SERVICE_DOMAIN=getenv('BACKEND_SERVICE_DOMAIN','http://127.0.0.1')
    BACKEND_SERVICE_PORT=getenv('BACKEND_SERVICE_PORT', 8001)