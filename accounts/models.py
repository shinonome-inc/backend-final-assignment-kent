from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False)


class FriendShip(models.Model):
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower.username} : {self.following.username}"
