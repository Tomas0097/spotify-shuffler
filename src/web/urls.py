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
    path("spotify-auth/", views.SpotifyAuthView.as_view(), name="spotify-auth"),
    path(
        "spotify-session-ended/",
        views.SpotifySessionEnded.as_view(),
        name="spotify-session-ended",
    ),
    path("spotify-logout/", views.SpotifyLogoutView.as_view(), name="spotify-logout"),
]
