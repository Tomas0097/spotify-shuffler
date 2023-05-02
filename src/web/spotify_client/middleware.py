from django.shortcuts import redirect
from django.urls import reverse

from web.spotify_client.exceptions import SpotifyUnauthorizedRequest


class SpotifyClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, SpotifyUnauthorizedRequest):
            return redirect(reverse("web:homepage"))

        return None
