# -*- coding: utf-8 -*-
'''
Created on Mar 14, 2016

@author: yufeitan
'''
from game_process.models import User, Room, UserInRoomIdentity, Record
import random
from datetime import datetime,timedelta
from resist_organization.models import vote_result, vote
def get_syies_count(totalCount):
    if totalCount >= 5 and totalCount <= 6:
        return 2
    elif totalCount >= 7 and totalCount <= 9:
        return 3
    elif totalCount >= 10 and totalCount <= 12:
        return 4
    else:
        return -1

def how_many_user_vote(vote_sequence,total_user_count):
    if vote_sequence ==1:
        if total_user_count<=7:
            return 2
        else:
            return 3
    elif vote_sequence == 2:
        if total_user_count <= 7:
            return 3
        else:
            return 4
    elif vote_sequence == 3:
        if total_user_count == 5:
            return 2
        elif total_user_count==7:
            return 3
        else:
            return 4
    elif vote_sequence == 4:
        if total_user_count <= 6:
            return 3
        elif total_user_count ==7:
            return 4
        else:
            return 5
    elif vote_sequence==5:
        if total_user_count == 5:
            return 3
        elif total_user_count <=7:
            return 4
        else:
            return 5
        
def which_side_get_point(vote_sequence,totalUserCount,spy_vote_count):
    #return 1 means spies get this point ,otherwise returns 2
    if spy_vote_count == 0:
        return 2
    if vote_sequence==4 and totalUserCount>=7 :
        if spy_vote_count>=2:
            return 1
        else:
            return 2
    elif spy_vote_count >= 1 :
        return 1
    

def create_one_room(userCount,wait_type):
    room = Room(userCount=userCount,game_type=wait_type)
    while True:
        index = random.randint(1000, 9999)
        if Room.objects.filter(roomNum=index).count() > 0:
            continue
        room.roomNum = index
        allocation_identity(room, get_syies_count(userCount))
        room.save()
        break;
    return room;

def allocation_identity(room, howManySpies):
    identityList = set()
    while len(identityList) < howManySpies:
        identityList.add(random.randint(1, room.userCount))
    room.identityDistribution = ",".join(map(str, identityList))

"""The manager use this method to init a room"""
def init_room(userName, userCount,wait_type):
    user, existed = User.objects.get_or_create(userName=userName)
    room = create_one_room(userCount,wait_type)
    UserInRoomIdentity.objects.create(user=user, room=room, identity="manager", number=0 , aliveOrDead=0)
    return room
    
def join_room(userName, roomNum):
    room = Room.objects.filter(roomNum=roomNum)
    bool(room)
    if room.count() == 0:
        return None,u"房间不存在"
    user, existed = User.objects.get_or_create(userName=userName)
    usersInRoomNow = UserInRoomIdentity.objects.filter(room=room[0]).order_by("-number")[0].number
    if usersInRoomNow >= room[0].userCount:
        return None,u"房间已满"
    # this user is already in that room
    current = UserInRoomIdentity.objects.filter(user=user, room=room[0])
    if current.count() > 0 :
        return room[0],current[0]
    
    identity = "civilian"
    if str(usersInRoomNow + 1) in room[0].identityDistribution.split(","):
        identity = "spy"
    userInRoomIdentity = UserInRoomIdentity.objects.create(user=user, room=room[0], identity=identity, number=usersInRoomNow + 1 , aliveOrDead=1)
    return room[0],userInRoomIdentity

def vote_once(userName,vote_type):
    #vote_type:support/break
    userInRoomIdentity = UserInRoomIdentity.objects.get(user__userName=userName)
    latast_vote_result = vote_result.objects.filter(room=userInRoomIdentity.room)
    bool(latast_vote_result)
    current_vote_sequence = latast_vote_result.count()+1
    vote.objects.create(user=userInRoomIdentity.user,room=userInRoomIdentity.room,vote_sequence=current_vote_sequence,vote_content=vote_type)
    current_vote_result = calculate_one_round_result(current_vote_sequence)
    is_game_over,winner_side = whether_game_over(userInRoomIdentity.room)
    if is_game_over:
        clear_room(userInRoomIdentity.room)
        return True,winner_side
    else:
        return False,current_vote_result
    
def calculate_one_round_result(vote_sequence):
    vote_list = vote.objects.filter(vote_sequence=vote_sequence)
    bool(vote_list)
    totalUserCount = vote_list[0].room.userCount
    if vote_list.count() < how_many_user_vote(vote_sequence,totalUserCount):
        return None
    else:
        spies_vote_count = 0
        for each_vote in vote_list:
            if each_vote.vote_content == "break":
                spies_vote_count += 1
        
        if which_side_get_point(vote_sequence, totalUserCount, spies_vote_count) ==1:
            return vote_result.objects.create(room=vote_list[0].room,vote_sequence=vote_sequence,\
                                       spy_vote_count=spies_vote_count,\
                                       civilian_vote_count=how_many_user_vote(vote_sequence,totalUserCount)-spies_vote_count,\
                                       which_side_get_point="spy")
        else:
            return vote_result.objects.create(room=vote_list[0].room,vote_sequence=vote_sequence,\
                                       spy_vote_count=spies_vote_count,\
                                       civilian_vote_count=how_many_user_vote(vote_sequence,totalUserCount)-spies_vote_count,\
                                       which_side_get_point="civilian")
            
def whether_game_over(room):
    vote_result_list = vote_result.objects.filter(room=room)
    bool(vote_result_list)
    if vote_result_list.count() < 3:
        return False,None
    else:
        spies_win_count = 0
        civilian_win_count = 0
        for each_vote_result in vote_result_list:
            if each_vote_result.which_side_get_point == "spy":
                spies_win_count += 1
            else:
                civilian_win_count += 1
        if spies_win_count == 3:
            return True,"spy"
        elif civilian_win_count == 3:
            return True,"civilian"
        else:
            return False,None
    
#get all round result and current score situation
def get_current_situation(room):
    vote_result_list = vote_result.objects.filter(room=room).order_by("vote_sequence")
    spy_winned_count = 0
    civilian_winned_count = 0
    for each_vote_result in vote_result_list:
        if each_vote_result.which_side_get_point == "spy":
            spy_winned_count += 1
        else:
            civilian_winned_count += 1
    return civilian_winned_count,spy_winned_count,vote_result_list
    
#clear server data after game is over
def clear_room(room):
    Record.objects.create(userCount=room.userCount,modifiedTime=room.modifiedTime,game_type=room.game_type)
    room.delete()
    
    
    
    
    
    
    
    