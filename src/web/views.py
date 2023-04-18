import requests

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.utils.http import urlencode, urlsafe_base64_encode


class HomepageView(TemplateView):
    template_name = "homepage.html"

class SpotifyAuthView(View):
    def get(self, request, *args, **kwargs):
        client_id = "77aee9b86365440d8b2849e168d01dee"
        client_secret_key = "2bcf35e555234fa3a32ea87d28117cc7"
        redirect_uri = "http://localhost:8088/spotify-auth"

        authorization_code = request.GET.get("code")
        access_token = request.GET.get("access_token")
        error = request.GET.get("error")

        if authorization_code:
            url_encoded_parameters = urlencode({
                "code": authorization_code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            })
            spotify_access_token_url = "https://accounts.spotify.com/api/token"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + urlsafe_base64_encode(f"{client_id}:{client_secret_key}".encode())
            }

            response = requests.post(spotify_access_token_url, headers=headers, data=url_encoded_parameters)

            if response.status_code == 200:
                return HttpResponse()
            else:
                return HttpResponse()

        elif access_token:
            return HttpResponse()

        elif error:
            return HttpResponse()

        else:
            # TODO: The state should be randomly generated 16 character long string. Saving this value
            #       before requesting Spotify auth and verifying the match in the callback is very
            #       recommended by Spotify API documentation.
            state = "abcdefghijklmnop"
            scope = "user-read-private user-read-email"

            url_encoded_parameters = urlencode({
                "response_type": "code",
                "client_id": client_id,
                "scope": scope,
                "redirect_uri": redirect_uri,
                "state": state
            })
            spotify_auth_url = "https://accounts.spotify.com/authorize?" + url_encoded_parameters

            return HttpResponseRedirect(spotify_auth_url)