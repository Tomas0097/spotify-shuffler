from django.urls import path

from web.views import auth as auth_views
from web.views import main as main_views

app_name = "web"

urlpatterns = [
    path(
        "",
        main_views.HomepageView.as_view(),
        name="homepage",
    ),
    path(
        "profile/",
        main_views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "spotify-link-account/",
        auth_views.SpotifyLinkAccountView.as_view(),
        name="spotify-link-account",
    ),
    path(
        "spotify-session-error/",
        auth_views.SpotifySessionError.as_view(),
        name="spotify-session-error",
    ),
    path(
        "spotify-logout/",
        auth_views.SpotifyLogoutView.as_view(),
        name="spotify-logout",
    ),
]
