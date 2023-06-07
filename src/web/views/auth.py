import secrets
import string

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from web.spotify_client.exceptions import SpotifyAPIError
from web.views.main import SpotifyClientView


class SpotifyLinkAccountView(SpotifyClientView):
    def get(self, request, *args, **kwargs):
        start_auth = request.GET.get("start_auth")
        authorization_code = request.GET.get("code")
        returned_state = request.GET.get("state")
        stored_state = request.session.get("spotify_auth_state")

        if start_auth:
            state = self._generate_random_string()
            spotify_authorization_url = self.spotify_client.get_authorization_url()
            spotify_authorization_url += f"&state={state}"
            request.session["spotify_auth_state"] = state
            return HttpResponseRedirect(spotify_authorization_url)

        # Spotify API Authorization process sends an authorization
        # code if the user has login successfully.
        if authorization_code and returned_state == stored_state:
            user_access_token = self.spotify_client.get_user_access_token(
                authorization_code
            )
            request.session["user_access_token"] = user_access_token
            del request.session["spotify_auth_state"]
            return HttpResponseRedirect(reverse("web:profile"))

        else:
            raise SpotifyAPIError

    @staticmethod
    def _generate_random_string():
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(16))


class SpotifyLogoutView(View):
    def get(self, request):
        del request.session["user_access_token"]
        return HttpResponseRedirect(reverse("web:homepage"))
