# -*- coding: utf-8 -*-
'''
Created on Mar 10, 2016

@author: yufeitan
'''
from wechat_sdk.messages import TextMessage
from game_process.models import UserWaitForInitRoom, User, Room,\
    RoomPhraseRelation
from game_process.service import initRoom, joinRoom
from datetime import datetime

initRoomReply=u"""建房成功，请参与游戏人员直接输入房号【%d】加入游戏\n
                房号：  %d\n
                人数：  %d卧底  %d平民\n
                卧底词：  %s\n
                平民词：  %s\n
                卧底：  %s\n
                回复【换】，换一组词
                """
joinRoomReply=u"""成功加入%d房间\n
                你的词语为%s\n
                你的号码为%d\n
                """

def process_msg(message):
    if isinstance(message, TextMessage):
        content = message.content.strip()
        print content
        waitedUser = UserWaitForInitRoom.objects.filter(user__userName=message.source)
        bool(waitedUser)
        if waitedUser.count() > 0 and waitedUser[0].wait_type=="undercover":
            joinCount = 0
            try:
                joinCount = int(content)
            except:
                return "not number"
            if joinCount < 4 or joinCount > 15:
                return "must >4 <15"
            else:
                room,phrase = initRoom(message.source,joinCount)
                waitedUser.delete()
                return formatInitRoomReply(room,phrase)
        else:
            if content == "1" :
                user,existed = User.objects.get_or_create(userName=message.source)
                UserWaitForInitRoom.objects.get_or_create(user=user,wait_type="undercover",wait_time=datetime.now())
                return u"谁是卧底，请输入游戏人数4-15"
            elif Room.objects.filter(roomNum=int(content)).count()>0 :
                room,identity = joinRoom(message.source,int(content))
                #if room is none , then identity is message from lower level
                if room == None:
                    return identity
                return formateJoinRoom(room,identity)
                
def formatInitRoomReply(room,phrase):
    undercoverCount = room.identityDistribution.split(",")
    return initRoomReply %(room.roomNum,room.roomNum,len(undercoverCount),room.userCount-len(undercoverCount)\
                           ,phrase.firstPhrase,phrase.secondPhrase,room.identityDistribution)
    
def formateJoinRoom(room,identity):
    phraseEntry = RoomPhraseRelation.objects.get(room=room).phrase
    phrase = ""
    if identity.identity == "civilian":
        phrase = phraseEntry.firstPhrase
    elif identity.identity == "undercover":
        phrase = phraseEntry.secondPhrase
    print room.roomNum,phrase,identity.number
    return joinRoomReply %(room.roomNum,phrase,identity.number)
    
    
    
    
    
    