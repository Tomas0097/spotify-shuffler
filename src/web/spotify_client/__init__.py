import requests
from requests.models import Response

from django.utils.http import urlencode, urlsafe_base64_encode

from web.models import Configuration
from web.spotify_client.exceptions import SpotifyAPIError, SpotifyAPIUnauthenticatedUser


class SpotifyClient:
    def __init__(self, user_access_token=""):
        config = Configuration.objects.last()
        self.api_url = config.spotify_api_url
        self.client_id = config.spotify_client_id
        self.client_secret_key = config.spotify_client_secret_key
        self.api_scope = config.spotify_api_scope
        self.redirect_uri = config.spotify_redirect_uri
        self.user_access_token = user_access_token

    @staticmethod
    def _send_request(method, url, headers, data=None) -> Response:
        response = requests.request(method, url, headers=headers, data=data)

        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            raise SpotifyAPIUnauthenticatedUser()
        else:
            raise SpotifyAPIError()

        return response

    def _get_data(self, endpoint) -> dict:
        headers = {"Authorization": "Bearer " + self.user_access_token}
        response = self._send_request("get", endpoint, headers)

        return response.json()

    def get_authorization_url(self) -> str:
        params = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "scope": self.api_scope,
                "redirect_uri": self.redirect_uri,
            }
        )

        return "https://accounts.spotify.com/authorize?" + params

    def get_user_access_token(self, authorization_code) -> str:
        endpoint = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic "
            + urlsafe_base64_encode(
                f"{self.client_id}:{self.client_secret_key}".encode()
            ),
        }
        data = {
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response = self._send_request("post", endpoint, headers=headers, data=data)

        return response.json()["access_token"]

    def get_user_profile_data(self) -> dict:
        endpoint = self.api_url + "me"

        return self._get_data(endpoint)
