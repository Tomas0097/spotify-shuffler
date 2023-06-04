from django.db import models
from django.utils.translation import gettext_lazy as _


class Configuration(models.Model):
    spotify_api_url = models.CharField(
        verbose_name=_("Spotify API Url"),
        max_length=50
    )
    spotify_client_id = models.CharField(
        verbose_name=_("Spotify Client ID"),
        max_length=50
    )
    spotify_client_secret_key = models.CharField(
        verbose_name=_("Spotify Client Secret Key"),
        max_length=50
    )
    spotify_api_scope = models.CharField(
        verbose_name=_("Spotify API Scope"),
        max_length=800
    )
    spotify_redirect_uri = models.CharField(
        verbose_name=_("Spotify Redirect Uri"),
        max_length=100
    )

    def __str__(self):
        return f"Configuration {self.id}"

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")
