from django.urls import path

from web import views


app_name = "web"

urlpatterns = [
    path(
        "",
        views.HomepageView.as_view(),
        name="homepage",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("spotify-link-account/", views.SpotifyLinkAccountView.as_view(), name="spotify-link-account"),
    path(
        "spotify-session-error/",
        views.SpotifySessionError.as_view(),
        name="spotify-session-error",
    ),
    path("spotify-logout/", views.SpotifyLogoutView.as_view(), name="spotify-logout"),
]
