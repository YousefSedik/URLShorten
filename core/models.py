from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import uuid


class AffiliateSource(models.Model):
    affiliate_source = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url_shortener = models.ForeignKey("URLShortener", on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["affiliate_source"]),
            models.Index(fields=["url_shortener"]),
        ]

    def __str__(self):
        return f"{self.affiliate_source} - {self.url_shortener.original_url}"


class URLShortener(models.Model):
    short_url_key = models.UUIDField(
        unique=True, primary_key=True, editable=False, default=uuid.uuid4
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    @property
    def shorten_url(self):
        return settings.DEFAULT_DOMAIN + reverse(
            "url_redirect_api_view", kwargs={"short_url_key": self.short_url_key}
        )

    def __str__(self):
        return self.original_url
