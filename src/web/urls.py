from django.urls import include, path

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
]
