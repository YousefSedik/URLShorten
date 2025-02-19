from django.urls import path
from .api import url_shorten_create_api_view, url_redirect_api_view

urlpatterns = [
    path("<uuid:short_url_key>/", url_redirect_api_view, name="url_redirect_api_view"),
    path("shorten/", url_shorten_create_api_view, name="url_shorten_create_api_view"),
]
