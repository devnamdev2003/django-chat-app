from django.db import models
from django.contrib.auth.models import User


class UserRelation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_relations"
    )
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_relations", default=None
    )  # Change default as needed
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
