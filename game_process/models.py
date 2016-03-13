from django.db import models
import datetime

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
    modifiedTime = models.DateTimeField(default=datetime.datetime.now())
    
class RoomPhraseRelation(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    phrase = models.ForeignKey(PhraseEntry)
    
class UserInRoomIdentity(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    identity = models.CharField(max_length=10)
    number = models.IntegerField()
    # alive for 1,dead for 2
    aliveOrDead = models.IntegerField(null=True)
    
    def __unicode__(self):
        return self.identity+" "+str(self.number)+" "+str(self.aliveOrDead)
    
class Record(models.Model):
    userCount = models.IntegerField()
    modifiedTime = models.DateTimeField()
    phrase_entry = models.ForeignKey(PhraseEntry,on_delete=models.SET_NULL,null=True)
    
class UserWaitForInitRoom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wait_type = models.CharField(max_length=20)
    wait_time = models.DateTimeField(default=datetime.datetime.now())