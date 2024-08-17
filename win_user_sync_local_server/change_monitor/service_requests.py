"""
This module contains the RemoteServiceClient class for making remote service requests.
"""

import requests

from win_user_sync_local_server.user_groups.usergroups_scripts import Usergroup
from win_user_sync_local_server.users.user_scripts import User


class RemoteServiceClient:
    """Client for making requests to the remote service."""

    def __init__(self, host, token):
        self.base_url = f'http://{host}'
        self.auth_headers = {'Authorization': f'token {token}'}

    def get_usergroups(self, endpoint):
        """Fetch user groups from the remote service."""
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, headers=self.auth_headers)
            response.raise_for_status()
            data = response.json()
            usergroups = []

            for usergroup_data in data:
                name = usergroup_data.get('name', '')
                description = usergroup_data.get('description', '')
                users_data = usergroup_data.get('users', [])
                users = [User(user.get('username')) for user in users_data]
                usergroup = Usergroup(name, description, users)
                usergroups.append(usergroup)

            return usergroups
        except requests.exceptions.RequestException as exc:
            print(f"Error fetching user groups: {exc}")
            return []

    def get_blacklist(self, endpoint, client_id):
        """Fetch blacklist from the remote service."""
        url = f'{self.base_url}/{endpoint}/{client_id}'
        try:
            response = requests.get(url, headers=self.auth_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            print(f"Error fetching blacklist: {exc}")
            return []

    def trigger_sync(self, endpoint, data=None):
        """Trigger a sync operation on the remote service."""
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.post(url, json=data, headers=self.auth_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            print(f"Error triggering sync: {exc}")
            return None
