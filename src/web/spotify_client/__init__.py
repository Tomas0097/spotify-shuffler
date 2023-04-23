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

    # TODO: Rename to '_fetch_data'
    def _send_request(self, url: str) -> dict:
        if self.access_token:
            headers = {"Authorization": "Bearer " + self.access_token}
            response = requests.get(url, headers=headers)
            response_data = response.json()

            return response_data
        else:
            # TODO: Handle this error.
            pass

    def get_user_profile(self) -> dict:
        endpoint = self.api_url + "me"
        data = self._send_request(endpoint)

        return data

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

    def get_access_token(self, authorization_code):
        url_encoded_parameters = urlencode(
            {
                "code": authorization_code,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            }
        )
        spotify_access_token_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + urlsafe_base64_encode(f"{self.client_id}:{self.client_secret_key}".encode()),
        }
        response = requests.post(
            spotify_access_token_url, headers=headers, data=url_encoded_parameters
        )

        if response.status_code == 200:
            response_data = response.json()

            return response_data["access_token"]

        else:
            # TODO: Handle this error.
            pass
