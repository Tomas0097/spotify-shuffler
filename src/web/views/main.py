from django.views.generic import TemplateView

from web.spotify_client import SpotifyClient
from web.views.auth import SpotifyClientErrorHandlerMixin


class HomepageView(TemplateView):
    template_name = "homepage.html"


class ProfileView(SpotifyClientErrorHandlerMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        user_access_token = self.request.session.get("user_access_token", "")
        spotify_client = SpotifyClient(user_access_token=user_access_token)
        profile_data = spotify_client.get_user_profile_data()
        context_data = super().get_context_data(**kwargs)
        context_data.update({"profile_name": profile_data["display_name"]})

        return context_data
