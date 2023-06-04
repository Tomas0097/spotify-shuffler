from django.contrib import admin

from web.models import Configuration


@admin.register(Configuration)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "SPOTIFY API SETTINGS",
            {
                "fields": (
                    "spotify_api_url",
                    "spotify_client_id",
                    "spotify_client_secret_key",
                    "spotify_api_scope",
                    "spotify_redirect_uri",
                )
            }
        ),
    )
