from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from web.spotify_client import SpotifyClient
from web.spotify_client.exceptions import SpotifyAPIError


class SpotifyClientErrorHandlerMixin:
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except SpotifyAPIError:
            return redirect(reverse("web:spotify-session-error"))


class SpotifyLinkAccountView(View):
    def get(self, request):
        authorization_code = request.GET.get("code")
        error = request.GET.get("error")

        if authorization_code:
            user_access_token = SpotifyClient().get_user_access_token(
                authorization_code
            )
            request.session["user_access_token"] = user_access_token

            return HttpResponseRedirect(reverse("web:profile"))

        # TODO: Handle this error.
        elif error:
            return HttpResponse()

        else:
            spotify_authorization_url = SpotifyClient().get_authorization_url()

            return HttpResponseRedirect(spotify_authorization_url)


class SpotifyLogoutView(View):
    def get(self, request):
        del request.session["user_access_token"]

        return HttpResponseRedirect(reverse("web:homepage"))


class SpotifySessionError(TemplateView):
    template_name = "spotify-session-error.html"
