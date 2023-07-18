import requests
from requests.models import Response

from django.utils.http import urlencode, urlsafe_base64_encode

from web.models import Configuration
from web.spotify_client.exceptions import SpotifyAPIError, SpotifyAPIUnauthenticatedUser


class SpotifyClient:
    def __init__(self, user_access_token=""):
        config = (
            Configuration.objects.last()
        )  # todo: Handle situation where model Configuration doesn't have any record.
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

    def get_user_playlists_data(self) -> dict:
        endpoint = self.api_url + "me/playlists"

        return self._get_data(endpoint)

    def get_playlist_data(self, playlist_id) -> dict:
        endpoint_playlist = self.api_url + f"playlists/{playlist_id}"
        playlist_data = self._get_data(endpoint_playlist)
        playlist_tracks_total = playlist_data["tracks"]["total"]

        playlist_tracks_data = []
        offset = 0

        # Spotify API limits track retrieval to 50 per request, requiring
        # multiple requests for playlists with over 50 tracks.
        while playlist_tracks_total > offset:
            query_offset = f"offset={offset}"
            query_fields = "fields=items(track(id, name, artists(name)))"
            endpoint_playlist_tracks_batch = (
                self.api_url
                + f"playlists/{playlist_id}/tracks?{query_offset}&{query_fields}"
            )
            playlist_tracks_batch_data = self._get_data(endpoint_playlist_tracks_batch)
            playlist_tracks_data.extend(playlist_tracks_batch_data["items"])
            offset += 100

        playlist_data["tracks"]["items"] = playlist_tracks_data

        return playlist_data
