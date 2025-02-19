from rest_framework import serializers
from .models import URLShortener


class URLShortenerSerializer(serializers.ModelSerializer):
    shorten_url = serializers.SerializerMethodField()
    class Meta:
        model = URLShortener
        fields = ["original_url", "shorten_url",]
    
    def get_shorten_url(self, obj):
        return obj.shorten_url
