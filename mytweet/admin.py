from django.contrib import admin
from .models import Tweet 


class TweetAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "user__email"]
    
    list_display = ['id', 'user','content']
    
    filter_fields = ['user', 'content']
    class Meta:
        Model = Tweet 
admin.site.register(Tweet, TweetAdmin)

