import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',')]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = bool(os.getenv('CACHE', False))
DEBUG = bool(os.getenv('DEBUG', False))
DEBUG_TOOLBAR = bool(os.getenv('DEBUG_TOOLBAR', False) and DEBUG)
INTERNAL_IPS = ['127.0.0.1', ]
SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG and bool(os.getenv('SECURE_SSL_REDIRECT', False))

SESSION_COOKIE_SECURE = not DEBUG and bool(os.getenv('SESSION_COOKIE_SECURE', False))
SESSION_COOKIE_HTTPONLY = SESSION_COOKIE_SECURE
CSRF_COOKIE_HTTPONLY = SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', 31536000))

IPG_API_KEY = os.getenv('IPG_API_KEY')
IPG_API_VERSION = os.getenv('IPG_API_VERSION')
IPG_PAYMENT_ALL_DYNAMIC = os.getenv('IPG_PAYMENT_ALL_DYNAMIC')
IPG_REQUIRE_COMPLETE = os.getenv('IPG_REQUIRE_COMPLETE')
IPG_STORE_ID = os.getenv('IPG_STORE_ID')
IPG_TRANSACTION_STATUS_ENDPOINT = os.getenv('IPG_TRANSACTION_STATUS_ENDPOINT')
IPG_URL = os.getenv('IPG_URL')
PKCS12_FILENAME = os.getenv('PKCS12_FILENAME')
PKCS12_PASSWORD = os.getenv('PKCS12_PASSWORD')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'webpack_loader',
    'rest_framework',
    'anymail',

    'account.apps.AccountConfig',
    'django.contrib.admin',

    'thebrushstash.apps.TheBrushStashConfig',
    'shop.apps.ShopConfig',
]

if DEBUG:
    INSTALLED_APPS.insert(7, 'django_extensions')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'thebrushstash.middleware.LocaleMiddlewareOverride',
    'thebrushstash.middleware.set_currency_middleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS.insert(6, 'debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

if CACHE:
    MIDDLEWARE.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': None,
        }
    }
    LOADERS = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    CACHE_MIDDLEWARE_KEY_PREFIX = 'thebrushstash_'
    CACHE_MIDDLEWARE_SECONDS = 315360000

ROOT_URLCONF = 'thebrushstash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': LOADERS,
        },
    },
]

WSGI_APPLICATION = 'thebrushstash.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '',
        'CONN_MAX_AGE': 600,
    }
}

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

# do not change, Django uses _language in request.session regardless of LANGUAGE_COOKIE_NAME
LANG_COOKIE_NAME_INTERNAL = '_language'
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('hr', 'Croatian'),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(
            BASE_DIR, 'webpack-stats{}.json'.format('-prod' if not DEBUG else '')
        ),
    }
}

AUTH_USER_MODEL = 'account.CustomUser'
ACTIVATION_RESET_TIMEOUT = int(os.getenv('ACTIVATION_RESET_TIMEOUT'))
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ANYMAIL = {
    'MAILGUN_API_KEY': os.getenv('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': os.getenv('MAILGUN_SENDER_DOMAIN'),
    'MAILGUN_API_URL': os.getenv('MAILGUN_API_URL'),
}
DEFAULT_FROM_EMAIL = 'The Brush Stash Webshop <webshop@mg.thebrushstash.com>'
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.com'
EMAIL_PORT = 587
EMAIL_USE_SSL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'COERCE_DECIMAL_TO_STRING': False,
}

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'class': 'django.utils.log.AdminEmailHandler',
                'level': 'ERROR',
            },
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(BASE_DIR, 'error.log')
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False,
            },
            'shop': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False
            },
            'thebrushstash': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False
            },
        },
    }
