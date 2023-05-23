from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from web.spotify_client import SpotifyClient
from web.spotify_client.exceptions import SpotifyAuthenticationError


class SpotifyAuthMixin:
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except SpotifyAuthenticationError:
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


class HomepageView(TemplateView):
    template_name = "homepage.html"


class ProfileView(SpotifyAuthMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        user_access_token = self.request.session.get("user_access_token", "")
        profile_data = SpotifyClient(
            user_access_token=user_access_token
        ).get_user_profile_data()

        context_data = super().get_context_data(**kwargs)
        context_data.update({"profile_name": profile_data["display_name"]})

        return context_data
