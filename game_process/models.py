from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.userName
    
class PhraseEntry(models.Model):
    firstPhrase = models.CharField(max_length=10)
    secondPhrase = models.CharField(max_length=10)
    
class Room(models.Model):
    roomNum = models.IntegerField()
    userCount = models.IntegerField()
    identityDistribution = models.CharField(max_length=10,null=True)
    
class RoomPhraseRelation(models.Model):
    room = models.ForeignKey(Room)
    phrase = models.ForeignKey(PhraseEntry)
    
class UserInRoomIdentity(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    identity = models.CharField(max_length=10)
    number = models.IntegerField()
    # alive for 1,dead for 2
    aliveOrDead = models.IntegerField(null=True)
    
