from rest_framework.generics import CreateAPIView, GenericAPIView
from .models import URLShortener, AffiliateSource
from .serializers import URLShortenerSerializer
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.db.models import F

# skip csrf token

class URLShortenAPIView(CreateAPIView):
    serializer_class = URLShortenerSerializer
    queryset = URLShortener.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


url_shorten_create_api_view = URLShortenAPIView.as_view()


class URLRedirectAPIView(GenericAPIView):
    serializer_class = URLShortenerSerializer
    queryset = URLShortener.objects.all()

    def get(self, request, *args, **kwargs):
        short_url_key = self.kwargs.get("short_url_key")
        affiliate_source = self.request.query_params.get("src")
        url_shortener = get_object_or_404(URLShortener, short_url_key=short_url_key)
        url_shortener.views += 1
        url_shortener.save()
        if affiliate_source and len(affiliate_source) <= 10:
            aff_source, created = AffiliateSource.objects.get_or_create(
                affiliate_source=affiliate_source,
                url_shortener=url_shortener,
                defaults={"views": 1}
            )
            if not created:
                AffiliateSource.objects.filter(pk=aff_source.pk).update(
                    views=F("views") + 1
                )
        return redirect(url_shortener.original_url)


url_redirect_api_view = URLRedirectAPIView.as_view()
