from django.contrib import admin
from .models import UserProfile, UserFavorite, UserMessage
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user','fav_id']
    search_fields = ['user', 'fav_id']


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'has_read']
    search_fields = ['user', 'title', 'message']
    list_filter = ['has_read']


admin.site.register(UserProfile, UserAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)

