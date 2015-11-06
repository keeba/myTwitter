from django.contrib.auth.models import User
from django.db import models

class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
    def __str__(self):
        return self.text    

class Followee(models.Model):
    follower = models.ForeignKey(User,related_name="follower")
    followee = models.ForeignKey(User,related_name="followee")
    def __str__(self):
        return self.follower.get_full_name()