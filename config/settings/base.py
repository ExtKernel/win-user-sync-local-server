import os
import subprocess
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def get_env_var(env_var):
    """
    Returns environment variables

    :param env_var:
    :return:
    """

    try:
        return os.environ[env_var]
    except KeyError as exc:
        error_msg = f"{exc}. Set the {env_var} environment variable"
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_powershell_path():
    """
    Returns the path to the PowerShell executable on the system.

    Uses the 'where' command to locate the PowerShell executable.

    Returns:
        str: The path to the PowerShell executable.
    """
    result = subprocess.run("where powershell", capture_output=True, text=True)
    powershell_path = result.stdout.strip()
    return powershell_path


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_keycloak_auth.middleware.KeycloakMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# The role that the OAuth2 user should have in the token to access secured endpoints
PRINCIPAL_ROLE_NAME = get_env_var('PRINCIPAL_ROLE_NAME')

# Config for idp-sync-service
# Visit the repository for more info
# https://github.com/ExtKernel/idp-sync-service
REMOTE_SERVICE_OAUTH2_TOKEN_URL = get_env_var('REMOTE_SERVICE_OAUTH2_TOKEN_URL')
REMOTE_SERVICE_OAUTH2_CLIENT_ID = get_env_var('REMOTE_SERVICE_OAUTH2_CLIENT_ID')
REMOTE_SERVICE_OAUTH2_CLIENT_SECRET = get_env_var('REMOTE_SERVICE_OAUTH2_CLIENT_SECRET')
REMOTE_SERVICE_OAUTH2_USERNAME = get_env_var('REMOTE_SERVICE_OAUTH2_USERNAME')
REMOTE_SERVICE_OAUTH2_PASSWORD = get_env_var('REMOTE_SERVICE_OAUTH2_PASSWORD')
