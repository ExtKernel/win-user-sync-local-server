import threading

from django.utils import timezone

from config.settings.base import (
    get_powershell_path,
    REMOTE_SERVICE_OAUTH2_TOKEN_URL,
    REMOTE_SERVICE_OAUTH2_CLIENT_ID,
    REMOTE_SERVICE_OAUTH2_CLIENT_SECRET,
    REMOTE_SERVICE_OAUTH2_USERNAME,
    REMOTE_SERVICE_OAUTH2_PASSWORD
)
from .models import RefreshToken
from .service_requests import RemoteServiceClient
from .tokens import TokenObtainer
from ..user_groups.usergroups_scripts import UsergroupRetriever

usergroup_retriever = UsergroupRetriever(get_powershell_path())
token_obtainer = TokenObtainer(
    REMOTE_SERVICE_OAUTH2_TOKEN_URL,
    REMOTE_SERVICE_OAUTH2_CLIENT_ID,
    REMOTE_SERVICE_OAUTH2_CLIENT_SECRET,
    REMOTE_SERVICE_OAUTH2_USERNAME,
    REMOTE_SERVICE_OAUTH2_PASSWORD
)


def monitor_change():
    refresh_token = RefreshToken.get_valid()
    remote = RemoteServiceClient(
        '192.168.122.7:8000',
        token_obtainer.get_access_token(refresh_token)
    )
    remote_usergroups = remote.get_usergroups('/secured/group')
    local_usergroups = usergroup_retriever.get_all()

    if len(remote_usergroups) != len(local_usergroups):
        remote.trigger_sync('/secured/sync/groups', local_usergroups)


timer = None


def start_interval_monitor(interval_in_sec):
    global timer
    timer = threading.Timer(interval_in_sec, monitor_change)
    timer.start()


def stop_interval_monitor():
    global timer
    if timer:
        timer.cancel()
