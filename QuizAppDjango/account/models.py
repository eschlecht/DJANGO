from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProfilePicture(models.Model):
    picture = models.FileField(null=True, blank=True)
    rank = models.IntegerField()


class UserRank(models.Model):
    rank = models.IntegerField()
    user_fk = models.ForeignKey(User)
    picture_id = models.IntegerField()
    total_score = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default='Beginner')
