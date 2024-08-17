"""
This module contains the Monitor class for monitoring user and group changes.
"""

import threading

from config.settings.base import (
    get_powershell_path,
    SERVER_NAME,
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
from ..users.views import user_retriever

usergroup_retriever = UsergroupRetriever(get_powershell_path())
token_obtainer = TokenObtainer(
    REMOTE_SERVICE_OAUTH2_TOKEN_URL,
    REMOTE_SERVICE_OAUTH2_CLIENT_ID,
    REMOTE_SERVICE_OAUTH2_CLIENT_SECRET,
    REMOTE_SERVICE_OAUTH2_USERNAME,
    REMOTE_SERVICE_OAUTH2_PASSWORD
)


def filter_by_blacklist(original, blacklist):
    """Filter out blacklisted entries from the original list."""
    return [entry for entry in original if entry not in blacklist]


class Monitor:
    """Monitor class for checking user and group changes."""

    def __init__(self):
        self.interval = None
        self.timer = None
        self.is_running = False

    def monitor_usergroup_change(self):
        """Monitor and sync user group changes."""
        try:
            refresh_token = RefreshToken.get_valid()
            remote = RemoteServiceClient(
                '192.168.122.7:8000',
                token_obtainer.get_access_token(refresh_token)
            )
            remote_usergroups = remote.get_usergroups('/secured/group')
            local_usergroups = usergroup_retriever.get_all()
            filtered_local_usergroups = filter_by_blacklist(
                local_usergroups,
                remote.get_blacklist('/secured/client/Win/usergroup-blacklist', SERVER_NAME)
            )

            if len(remote_usergroups) != len(filtered_local_usergroups):
                remote.trigger_sync('/secured/sync/groups', local_usergroups)
        except Exception as exc:
            print(f"Error in monitoring user group changes: {str(exc)}")

        # Schedule the next run if still running
        if self.is_running:
            self.timer = threading.Timer(self.interval, self.monitor_usergroup_change)
            self.timer.start()

    def monitor_user_change(self):
        """Monitor and sync user changes."""
        try:
            refresh_token = RefreshToken.get_valid()
            remote = RemoteServiceClient(
                '192.168.122.7:8000',
                token_obtainer.get_access_token(refresh_token)
            )
            remote_users = remote.get_usergroups('/secured/user')
            local_users = user_retriever.get_all()
            filtered_local_users = filter_by_blacklist(
                local_users,
                remote.get_blacklist('/secured/client/Win/user-blacklist', SERVER_NAME)
            )

            if len(remote_users) != len(filtered_local_users):
                remote.trigger_sync('/secured/sync/users', local_users)
        except Exception as exc:
            print(f"Error in monitoring user changes: {str(exc)}")

        # Schedule the next run if still running
        if self.is_running:
            self.timer = threading.Timer(self.interval, self.monitor_user_change)
            self.timer.start()

    def start_interval_monitor(self, interval_in_sec):
        """Start the interval monitor."""
        self.interval = interval_in_sec
        self.is_running = True
        # Start the first run immediately
        self.monitor_usergroup_change()
        self.monitor_user_change()

    def stop_interval_monitor(self):
        """Stop the interval monitor."""
        self.is_running = False
        if self.timer:
            self.timer.cancel()
            self.timer = None
