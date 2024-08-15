import requests

from win_user_sync_local_server.user_groups.usergroups_scripts import Usergroup
from win_user_sync_local_server.users.user_scripts import User


class RemoteServiceClient:
    def __init__(
            self,
            host,
            token
    ):
        self.base_url = f'http://{host}'
        self.authHeaders = {'Authorization': 'token {}'.format(token)}

    def get_usergroups(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, headers=self.authHeaders)
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
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user groups: {e}")
            return []

    def get_blacklist(self, endpoint, client_id):
        url = f'{self.base_url}/{endpoint}/{client_id}'
        try:
            response = requests.get(url, headers=self.authHeaders)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching blacklist: {e}")

    def trigger_sync(self, endpoint, data=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.post(url, json=data, headers=self.authHeaders)
        response.raise_for_status()

        return response.json()
