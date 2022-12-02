from django.contrib import admin

from accounts.models import User, FriendShip

admin.site.register(User)
admin.site.register(FriendShip)
