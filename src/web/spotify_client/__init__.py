import requests

class SpotifyClient:
    api_url = "https://api.spotify.com/v1/"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _send_request(self, url: str) -> dict:
        headers = {"Authorization": "Bearer " + self.access_token}
        response = requests.get(url, headers=headers)
        response_data = response.json()

        return response_data

    def get_user_profile(self) -> dict:
        endpoint = self.api_url + "me"
        data = self._send_request(endpoint)

        return data