from rest_framework import serializers
from django.conf import settings
from .models import Tweet 

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
class TweetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = ['content']
        
        def validate_content(self, value):
            if len(value) > MAX_TWEET_LENGTH:
                raise Serializers.ValidationsError("Tweet can't be more than 240 charracters")
            return value
            
            