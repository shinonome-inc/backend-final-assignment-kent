from django.contrib import admin

from accounts.models import FriendShip, User

admin.site.register(User)
admin.site.register(FriendShip)
