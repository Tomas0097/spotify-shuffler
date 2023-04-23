from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.urls import reverse

from web.spotify_client import SpotifyClient

class HomepageView(TemplateView):
    template_name = "homepage.html"


class SpotifyAuthView(View):
    def get(self, request, *args, **kwargs):
        authorization_code = request.GET.get("code")
        error = request.GET.get("error")

        if authorization_code:
            user_access_token = SpotifyClient().get_access_token(authorization_code)
            request.session["access_token"] = user_access_token

            return HttpResponseRedirect(reverse("web:profile"))

        # TODO: Handle this error.
        elif error:
            return HttpResponse()

        else:
            spotify_authorization_url = SpotifyClient().get_authorization_url()

            return HttpResponseRedirect(spotify_authorization_url)


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        access_token = self.request.session.get("access_token")
        profile_data = SpotifyClient(access_token=access_token).get_user_profile()

        context_data = super().get_context_data(**kwargs)
        context_data.update({"profile_name": profile_data["display_name"]})

        return context_data

class SpotifyAPIView(View):
    def get(self, request, *args, **kwargs):
        pass