from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse

from web.spotify_client import SpotifyClient
from web.spotify_client.exceptions import SpotifyAPIError, SpotifyAPIUnauthenticatedUser


class SpotifyClientMixin:
    spotify_client: SpotifyClient

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        user_access_token = request.session.get("user_access_token", "")
        self.spotify_client = SpotifyClient(user_access_token=user_access_token)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except SpotifyAPIError:
            return redirect(reverse("web:spotify-api-error"))
        except SpotifyAPIUnauthenticatedUser:
            return HttpResponseRedirect(reverse("web:spotify-link-account"))


class SpotifyAPIErrorView(TemplateView):
    template_name = "spotify-api-error.html"


class HomepageView(TemplateView):
    template_name = "homepage.html"


class ProfileView(SpotifyClientMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        profile_data = self.spotify_client.get_user_profile_data()
        playlists_data = self.spotify_client.get_user_playlists_data()
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "profile_name": profile_data["display_name"],
                "playlists": playlists_data["items"],
            }
        )
        return context_data
