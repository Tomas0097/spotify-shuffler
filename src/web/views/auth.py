from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from web.spotify_client.exceptions import SpotifyAPIError
from web.views.main import SpotifyClientView


class SpotifyLinkAccountView(SpotifyClientView):
    def get(self, request, *args, **kwargs):
        authorization_code = request.GET.get("code")
        error = request.GET.get("error")

        # Spotify API Authorization process sends an authorization
        # code if the user has login successfully.
        if authorization_code:
            user_access_token = self.spotify_client.get_user_access_token(
                authorization_code
            )
            request.session["user_access_token"] = user_access_token
            return HttpResponseRedirect(reverse("web:profile"))

        elif error:
            raise SpotifyAPIError

        else:
            spotify_authorization_url = self.spotify_client.get_authorization_url()
            return HttpResponseRedirect(spotify_authorization_url)


class SpotifyLogoutView(View):
    def get(self, request):
        del request.session["user_access_token"]
        return HttpResponseRedirect(reverse("web:homepage"))
