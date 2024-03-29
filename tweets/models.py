from django.db import models

from accounts.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} ::: id is {str(Tweet.pk)}"

    class Meta:
        verbose_name_plural = "ツイート"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="tweet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.user.username}" likes "{self.tweet.content}"'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "tweet"], name="unique_favorite"),
        ]
