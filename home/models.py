from django.db import models
from django.contrib.auth.models import User


# class UserRelation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     friendid = models.IntegerField(unique=True)
#     accepted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.friendid}"
