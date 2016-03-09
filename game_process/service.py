'''
@author: wolf
'''
from game_process.models import User, Room, PhraseEntry, RoomPhraseRelation, UserInRoomIdentity
import random
def getRandomPhrase():
    randomIndex = random.randint(0, PhraseEntry.objects.all().count() - 1)
    return PhraseEntry.objects.all()[randomIndex:randomIndex+1][0]
def createOneRoom(userCount):
    room = Room(userCount=userCount)
    while True:
        index = random.randint(1000, 9999)
        if Room.objects.filter(roomNum=index).count()>0:
            continue
        room.roomNum = index
        allocationIdentity(room,howManyUndercover(userCount))
        room.save()
        break;
    return room;
def allocationIdentity(room,howManyUndercouver):
    identityList = set()
    while len(identityList) < howManyUndercouver:
        identityList.add(random.randint(1,room.userCount))
    room.identityDistribution = ",".join(map(str, identityList))
def howManyUndercover(userCount):
    return 2
"""The manager use this method to init a room"""
def initRoom(userName, userCount):
    user,existed = User.objects.get_or_create(userName=userName)
    room = createOneRoom(userCount)
    UserInRoomIdentity.objects.create(user=user, room=room, identity="manager", number=0 , aliveOrDead=0)
    initPhrase = getRandomPhrase()
    RoomPhraseRelation.objects.create(room=room, phrase=initPhrase)
    
def joinRoom(userName,roomNum):
    room = Room.objects.filter(roomNum=roomNum)
    if room.count() == 0:
        return
    user,existed = User.objects.get_or_create(userName=userName)
    usersInRoomNow = UserInRoomIdentity.objects.filter(room=room[0]).order_by("-number")[0].number
    #this user is already in that room
    if UserInRoomIdentity.objects.filter(user=user,room=room[0]).count() > 0 :
        return
    
    identity = "civilian"
    if str(usersInRoomNow+1) in room[0].identityDistribution.split(","):
        identity = "undercover"
    UserInRoomIdentity.objects.create(user=user, room=room[0], identity=identity, number=usersInRoomNow+1 ,aliveOrDead=1)
    
def killOnePerson(userNum,roomNum):
    userStatus = UserInRoomIdentity.objects.filter(room__roomNum=roomNum,number=userNum)
    if userStatus.count() != 1:
        return
    if userStatus[0].aliveOrDead == 2:
        return
    userStatus[0].update(aliveOrDead=2)
        
    
    
    
    