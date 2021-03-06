# -*- coding: utf-8 -*-
from django.shortcuts import render
from wechat_sdk.messages import TextMessage
from game_process.models import User, UserInRoomIdentity, UserWaitForInitRoom,\
    Room
from resist_organization.models import vote, vote_result
import datetime
from resist_organization import wechat
from resist_organization.service import init_room, join_room, vote_once,\
    get_current_situation, clear_room
import re
from guess_word.views import get_rondom_word

# Create your views here.
def process_msg(message):
    if isinstance(message, TextMessage):
        content = message.content.strip()
        user,user_existed = User.objects.get_or_create(userName=message.source)
        if content == u"抵抗组织":
            UserInRoomIdentity.objects.filter(user=user).delete()
            vote.objects.filter(user=user).delete()
            
            userWaitForInitRoom,existed = UserWaitForInitRoom.objects.get_or_create(user=user)
            userWaitForInitRoom.wait_type = "resist_organization"
            userWaitForInitRoom.wait_time = datetime.datetime.now()
            userWaitForInitRoom.save()
            return wechat.waitForInitRoomReply
        if content == u"战况":
            userInRoomIdentity = UserInRoomIdentity.objects.filter(user=user)
            bool(userInRoomIdentity)
            if userInRoomIdentity.count()==0:
                return u"你尚未加入任何游戏"
            civilian_winned,spy_winned,vote_result_list = get_current_situation(userInRoomIdentity[0].room)
            return wechat.formate_query_reply(civilian_winned, spy_winned, vote_result_list)
        if content == u"规则":
            return wechat.resist_organization_rule
        if content == u"结束":
            userInRoomIdentity = UserInRoomIdentity.objects.filter(user=user)
            bool(userInRoomIdentity)
            if userInRoomIdentity.count() > 0 :
                clear_room(userInRoomIdentity[0].room)
        if content == u"猜词":
            return get_rondom_word()
        if content == u"换":
            return get_rondom_word()
        userWaitForInitRoom = UserWaitForInitRoom.objects.filter(user=user)
        bool(userWaitForInitRoom)
        if userWaitForInitRoom.count() > 0:
            if userWaitForInitRoom[0].wait_type == "resist_organization":
                return init_resist_organization_room(user,message,userWaitForInitRoom)
        elif re.match('^[\d]{4}$', content):
            want_join_room_num = int(content)
            room,msg = join_room(user,want_join_room_num)
            if room == None:
                return msg
            else:
                return wechat.formateJoinRoom(room, msg)
        elif UserInRoomIdentity.objects.filter(user=user).count()>0:
            is_game_over,result = None,None
            if content == u"支持":
                is_game_over,result = vote_once(user,"support")
            elif content == u"破坏":
                is_game_over,result = vote_once(user,"break")
            else:
                return wechat.vote_fail_reply
            
            if is_game_over:
                room = UserInRoomIdentity.objects.filter(user=user)[0].room
                civilian_winned,spy_winned,vote_result_list = get_current_situation(room)
                clear_room(room)
                return wechat.formate_game_over_reply(civilian_winned, spy_winned, vote_result_list)
            else:
                if result == None:
                    return u"等待本轮投票结束"
                else:
                    civilian_winned,spy_winned,round_result = get_current_situation(UserInRoomIdentity.objects.filter(user=user)[0].room)
                    return wechat.formateVoteReply(result,civilian_winned,spy_winned)
        else:
            return wechat.nothing_reply
                    
            
            
def init_resist_organization_room(user,message,userWaitForInitRoom):
    join_count = -1
    try:
        join_count = int(message.content.strip())
    except:
        return u"非数字，请输入5-12之间的数字"
    if join_count < 5 or join_count > 12:
        return u"请输入5-12之间的数字"
    room = init_room(user,join_count,userWaitForInitRoom[0].wait_type)
    userWaitForInitRoom.delete()
    return wechat.formatInitRoomReply(room)
    
def clear_user_data(user_name):
    UserInRoomIdentity.objects.filter(user__userName=user_name).delete()
    

    
    
    
    
    