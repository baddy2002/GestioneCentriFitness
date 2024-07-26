import sys
import dj_database_url
from os import getenv, path
from pathlib import Path
import dotenv 
from django.core.management.utils import get_random_secret_key
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env.local'

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


DEVELOPMENT_MODE = getenv("DEVELOPMENT_MODE", "False") == "True"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG", 'False') == 'True'

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOST", "127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',                              #cors per next js
    'rest_framework',                           #utilizzo rest_framework.simpleJWT
    'djoser',                                   #autenticazione jwt
    'storages',                                 #
    'gdstorage',                                #google drive per lo storage
    'social_django',                            #OAuth2 protocol(Google, Facebook, etc..)
    'users'                                     
]   

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SSO.urls'

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

WSGI_APPLICATION = 'SSO.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'GestioneCentriFitness_Users',
            'USER': 'postgres',
            'PASSWORD': 'password123',
            'HOST': 'localhost',
            'PORT': '5858'
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if getenv("DATABASE_URL", None) is None:
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

# Optional: If you have additional static files directories

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'USERNAME_RESET_CONFIRM_URL': 'username-reset/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': getenv('REDIRECT_URLS').split(','),
    'SERIALIZERS': {
        'token_obtain_pair': 'users.authentication.CustomTokenObtainPairSerializer',
    },
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET= getenv('GOOGLE_AUTH_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name']

SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY = getenv('FACEBOOK_AUTH_KEY')
SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET= getenv('FACEBOOK_AUTH_SECRET')
SOCIAL_AUTH_FACEBOOK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_PARAMS = {
    'fields': 'email, first_name'
}



AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60*60*24  
AUTH_COOKIE_SECURE = getenv("AUTH_COOKIE_SECURE", 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None' 
if DEVELOPMENT_MODE:
    BACKEND_SERVICE_PROTOCOL='http'
    BACKEND_SERVICE_DOMAIN='127.0.0.1'
    BACKEND_SERVICE_PORT=8000
else:
    BACKEND_SERVICE_PROTOCOL=getenv('BACKEND_SERVICE_PROTOCOL', 'http')
    BACKEND_SERVICE_DOMAIN=getenv('BACKEND_SERVICE_DOMAIN','127.0.0.1')
    BACKEND_SERVICE_PORT=getenv('BACKEND_SERVICE_PORT', 8000)
CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:8001,http://localhost:8001').split(',')
CORS_ALLOW_CREDENTIALS = True
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.UserAccount"


#Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DOMAIN = getenv('DOMAIN')
SITE_NAME = 'GestioneCentriFitness-SSO'
APPEND_SLASH=False


GS_BUCKET_NAME = 'GestioneCentriFitness'

DEFAULT_FILE_STORAGE = 'users.backends.GoogleDriveStorage'


KAFKA_BOOTSTRAP_SERVERS_READERS = [getenv('KAFKA_BOOTSTRAP_SERVERS_READERS','localhost:9092')]
KAFKA_TOPIC_READERS = getenv('KAFKA_TOPIC_READERS','employee-invitation')

KAFKA_BOOTSTRAP_SERVERS_WRITERS = [getenv('KAFKA_BOOTSTRAP_SERVERS_WRITERS','localhost:9092')]
KAFKA_TOPIC_WRITERS = getenv('KAFKA_TOPIC_WRITERS','invitation-status')