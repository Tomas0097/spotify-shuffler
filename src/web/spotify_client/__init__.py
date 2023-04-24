import requests

from django.utils.http import urlencode, urlsafe_base64_encode


class SpotifyClient:
    api_scope = "user-read-private user-read-email"
    api_url = "https://api.spotify.com/v1/"
    client_id = "77aee9b86365440d8b2849e168d01dee"
    client_secret_key = "2bcf35e555234fa3a32ea87d28117cc7"
    redirect_uri = "http://localhost:8088/spotify-auth"

    def __init__(self, access_token=None):
        self.access_token = access_token

    def _send_request(
        self, method: str, url: str, data=None, authorization=False
    ) -> dict:
        if self.access_token:
            headers = {"Authorization": "Bearer " + self.access_token}

        elif authorization:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic "
                + urlsafe_base64_encode(
                    f"{self.client_id}:{self.client_secret_key}".encode()
                ),
            }

        else:
            # TODO: Handle this error.
            return {}

        response = requests.request(method, url, headers=headers, data=data)

        return response.json()

    def get_authorization_url(self) -> str:
        # TODO: The state should be randomly generated 16 character long string. Saving this value
        #       before requesting Spotify auth and verifying the match in the callback is very
        #       recommended by Spotify API documentation.
        state = "abcdefghijklmnop"
        url_encoded_parameters = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "scope": self.api_scope,
                "redirect_uri": self.redirect_uri,
                "state": state,
            }
        )

        return "https://accounts.spotify.com/authorize?" + url_encoded_parameters

    def get_access_token(self, authorization_code) -> str:
        access_token_url = "https://accounts.spotify.com/api/token"
        data = {
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response_data = self._send_request(
            "post", access_token_url, data=data, authorization=True
        )

        return response_data["access_token"]

    def get_user_profile(self) -> dict:
        endpoint = self.api_url + "me"

        return self._send_request("get", endpoint)
