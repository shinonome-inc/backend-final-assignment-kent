from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False)


class FriendShip(models.Model):
    # フォロー関係：follower→followee
    # フォローをするユーザー
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    # フォロー対象のユーザー
    followee = models.ForeignKey(
        User, related_name="followee", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.follower.username}" follows "{self.followee.username}"'

    class Meta:
        constraints = [
            # 同じ日に部屋の予約を重複させない
            models.UniqueConstraint(
                fields=["follower", "followee"], name="unique_booking"
            ),
        ]
