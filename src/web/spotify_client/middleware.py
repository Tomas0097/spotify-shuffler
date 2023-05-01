from django.shortcuts import redirect
from django.urls import reverse

from django.http.response import HttpResponse

from web.spotify_client.exceptions import SpotifyUnauthorizedRequest

class SpotifyClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            print("Custom middleware - 1")

        except SpotifyUnauthorizedRequest:

            print("Custom middleware - 2")

            # return redirect(reverse("web:homepage"))
            HttpResponse()

        return response