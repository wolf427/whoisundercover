from __future__ import unicode_literals

from django.db import models

# Create your models here.
from game_process.models import Room,UserInRoomIdentity,User


class vote(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    vote_sequence = models.IntegerField()
    vote_content = models.CharField(max_length=10)
    
    
class vote_result(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    vote_sequence = models.IntegerField()
    spy_vote_count = models.IntegerField()
    civilian_vote_count = models.IntegerField()
    which_side_get_point = models.CharField(max_length=10)
    
    
    