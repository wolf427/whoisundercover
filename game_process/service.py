# -*- coding: utf-8 -*-
'''
@author: wolf
'''
from game_process.models import User, Room, PhraseEntry, RoomPhraseRelation, UserInRoomIdentity, Record
import random
from datetime import datetime,timedelta
def getUndercoverCount(totalCount):
    if totalCount >= 3 and totalCount <= 4:
        return 1
    elif totalCount >= 5 and totalCount <= 9:
        return 2
    elif totalCount >= 10 and totalCount <= 13:
        return 3
    elif totalCount >= 14 and totalCount <= 15:
        return 4
    else:
        return 4
    
def getRandomPhrase():
    randomIndex = random.randint(0, PhraseEntry.objects.all().count() - 1)
    return PhraseEntry.objects.all()[randomIndex:randomIndex + 1][0]

def create_one_room(userCount):
    room = Room(userCount=userCount)
    while True:
        index = random.randint(1000, 9999)
        if Room.objects.filter(roomNum=index).count() > 0:
            continue
        room.roomNum = index
        allocation_identity(room, getUndercoverCount(userCount))
        room.save()
        break;
    return room;

def allocation_identity(room, howManyUndercouver):
    identityList = set()
    while len(identityList) < howManyUndercouver:
        identityList.add(random.randint(1, room.userCount))
    room.identityDistribution = ",".join(map(str, identityList))

"""The manager use this method to init a room"""
def initRoom(userName, userCount):
    user, existed = User.objects.get_or_create(userName=userName)
    room = create_one_room(userCount)
    UserInRoomIdentity.objects.create(user=user, room=room, identity="manager", number=0 , aliveOrDead=0)
    initPhrase = getRandomPhrase()
    RoomPhraseRelation.objects.create(room=room, phrase=initPhrase)
    return room,initPhrase
    
def joinRoom(userName, roomNum):
    room = Room.objects.filter(roomNum=roomNum)
    bool(room)
    if room.count() == 0:
        return None,"房间不存在"
    user, existed = User.objects.get_or_create(userName=userName)
    usersInRoomNow = UserInRoomIdentity.objects.filter(room=room[0]).order_by("-number")[0].number
    if usersInRoomNow >= room[0].userCount:
        return None,"房间已满"
    # this user is already in that room
    current = UserInRoomIdentity.objects.filter(user=user, room=room[0])
    if current.count() > 0 :
        return room[0],current[0]
    
    identity = "civilian"
    if str(usersInRoomNow + 1) in room[0].identityDistribution.split(","):
        identity = "undercover"
    userInRoomIdentity = UserInRoomIdentity.objects.create(user=user, room=room[0], identity=identity, number=usersInRoomNow + 1 , aliveOrDead=1)
    return room[0],userInRoomIdentity
    
    
def killOnePerson(userNum, roomNum):
    userStatus = UserInRoomIdentity.objects.filter(room__roomNum=roomNum, number=userNum)
    bool(userStatus)  # this method cached the querySet,onterwise each userStatus[0] will load database once.
    if userStatus.count() != 1:
        return
    if userStatus[0].aliveOrDead == 2:
        return
    userStatus[0].aliveOrDead = 2
    userStatus[0].save()
    Room.objects.filter(roomNum=roomNum).update(modifiedTime=datetime.now())
    gameIsOver,msg = checkGameIsOver(roomNum)
    if gameIsOver:
        deleteOutdatedRecord(roomNum)
    
def checkGameIsOver(roomNum):
    allUserStatus = UserInRoomIdentity.objects.filter(room__roomNum=roomNum).exclude(number=0)
    bool(allUserStatus)
    totalPeopleCount = allUserStatus.count()
    undercoverCount = getUndercoverCount(totalPeopleCount)
    civilianCount = totalPeopleCount - undercoverCount
    for eachOne in allUserStatus:
        if eachOne.identity == "undercover" and eachOne.aliveOrDead == 2:
            undercoverCount -= 1
        if eachOne.identity == "civilian" and eachOne.aliveOrDead == 2:
            civilianCount -= 1
    msg = ""
    gameOver = False
    if undercoverCount == 0 :
        gameOver = True
        msg = "civilians win"
    elif undercoverCount + civilianCount < getUndercoverCount(totalPeopleCount) * 2 :
        gameOver = True
        msg = "undercovers win"
    return gameOver, msg

def deleteOutdatedRecord(roomNum):
    room = Room.objects.get(roomNum=roomNum)
    Record.objects.create(userCount=room.userCount, modifiedTime=room.modifiedTime, phrase_entry=RoomPhraseRelation.objects.get(room__roomNum=roomNum).phrase)
    room.delete()
    
def automicallyCleanUp():
    rooms = Room.objects.filter(modifiedTime__lt=(datetime.now()-timedelta(hours=1)))
    for room in rooms:
        if room.game_type == "resist_organization":
            Record.objects.create(userCount=room.userCount, modifiedTime=room.modifiedTime, game_type=room.game_type)
    rooms.delete()



