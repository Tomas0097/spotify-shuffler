from django.urls import include, path

from web import views


app_name = "web"

urlpatterns = [
    path(
        "",
        views.HomepageView.as_view(),
        name="homepage",
    )
]