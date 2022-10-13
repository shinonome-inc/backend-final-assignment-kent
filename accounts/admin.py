from django.contrib import admin

from .models import User


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, PostAdmin)
