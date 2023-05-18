from django.shortcuts import redirect
from django.urls import reverse

from web.spotify_client.exceptions import SpotifyWrongResponse


class SpotifyClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, SpotifyWrongResponse):
            return redirect(reverse("web:spotify-session-error"))

        return None
