from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'win_user_sync_local_server.user_groups.apps.UserGroupsConfig',
    'win_user_sync_local_server.users.apps.UsersConfig',
    'win_user_sync_local_server.change_monitor.apps.ChangeMonitorConfig',
    'win_user_sync_local_server.registry.apps.RegistryConfig',

    # Third-party
    'rest_framework',
]

KEYCLOAK_CONFIG = {
    'KEYCLOAK_SERVER_URL': get_env_var('KC_HOST'),
    'KEYCLOAK_REALM': get_env_var('KC_REALM'),
    'KEYCLOAK_CLIENT_ID': get_env_var('KC_CLIENT_ID'),
    'KEYCLOAK_CLIENT_SECRET_KEY': get_env_var('KC_CLIENT_SECRET'),
    'KEYCLOAK_CACHE_TTL': 60,
    'LOCAL_DECODE': False,
}
