import requests

from .models import RefreshToken


class TokenObtainer:
    def __init__(
            self,
            oauth2_token_url,
            client_id,
            client_secret,
            username,
            password
    ):
        self.oauth2_token_url = oauth2_token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    def get_refresh_token(self):
        url = self.oauth2_token_url

        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get('refresh_token')
        token_expires_in = token_data.get('refresh_expires_in')

        # Save or update refresh token in the database
        refresh_token = RefreshToken(token=token, token_expires_in=token_expires_in)
        refresh_token.save()

        return token



    def get_access_token(self, refresh_token):
        url = self.oauth2_token_url

        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')

        return access_token
