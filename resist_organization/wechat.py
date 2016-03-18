# -*- coding: utf-8 -*-
'''
Created on Mar 14, 2016

@author: yufeitan
'''
resist_organization_rule=u"""游戏分【自由战士】与【间谍】两个阵营，五局三胜。每局执行一次任务，选出部分参与者投票（如八人局，第一轮选3人，第二轮选4人。。。），每局任务开始前讨论，由一人提出参与该任务人选并阐述理由，其他玩家也可依次对该方案做点评，一轮讨论后投票，超过半数同意则该方案通过，否则由下一玩家提出方案，直至有一种方案通过（都不通过则执行第一个方案）。任务执行者可选择投【支持】或是【破坏】，若最终该轮任务收到的“破坏”超过限制则任务失败（如八人局第一轮只要有一个“破坏”则任务失败，而第四轮则至少有两个“破坏”任务失败），任务失败间谍记一分，反之自由战士记一分，先赢得三分的队伍胜利。"""
initRoomReply=u"""建房成功，请参与游戏人员直接输入房号【%d】加入游戏
房号：  %d
人数：  %d间谍  %d自由战士
间谍：  %s
各局得分条件(破坏人数/投票人数)：
"""
joinRoomReply=u"""成功加入%d房间
你的身份为%s
你的号码为%d
%s
当你被选中投票时，直接回复【支持】（支持行动）或是【破坏】破坏行动，任何时候输入【战况】查看游戏过程"""
                
voteReply=u"""第【%d】轮投票结束，投票结果：
【%d】支持，【%d】破坏
本轮任务：%s
当前比分：%d：%d（战士：间谍）"""
waitForInitRoomReply=u"""抵抗组织创建成功，请输入游戏人数【5-12】"""
gameOverReply=u"""
游戏结束，%s胜利
最终比分：%d：%d（战：谍）
游戏过程如下：
轮数 战：谍 得分
"""
queryReply=u"""
当前比分：%d:%d
轮数 战：谍  得分方
"""
nothing_reply=u"""输入【抵抗组织】建立房间，输入【规则】查看游戏规则，任何时候输入【结束】结束当前游戏"""


def formatInitRoomReply(room):
    spiesCount = room.identityDistribution.split(",")
    
    return (initRoomReply %(room.roomNum,room.roomNum,len(spiesCount),room.userCount-len(spiesCount)\
                           ,room.identityDistribution))+get_point_requirement(room.userCount)
    
def formateJoinRoom(room,identity):
    identity_str = ""
    msg = ""
    if identity.identity == "spy":
        identity_str = u"间谍"
        msg = u"间谍号码为:"+room.identityDistribution
    elif identity.identity == "civilian":
        identity_str = u"自由战士"
    return joinRoomReply %(room.roomNum,identity_str,identity.number,msg)

def formateVoteReply(vote_result,civilian_winned,spy_winned):
    current_round_result = u"失败"
    if vote_result.which_side_get_point == "civilian":
        current_round_result = u"成功"
    return voteReply %(vote_result.vote_sequence,vote_result.civilian_vote_count,vote_result.spy_vote_count,current_round_result,civilian_winned,spy_winned)
    
def formate_game_over_reply(civilian_winned,spy_winned,vote_result_list):
    winner = u"自由战士"
    if spy_winned == 3:
        winner = u"间谍"
    final_result = gameOverReply %(winner,civilian_winned,spy_winned)
    
    for each_vote_result in vote_result_list:
        winner_side = u"战"
        if each_vote_result.which_side_get_point == "spy":
            winner_side = u"谍"
        final_result += (str(each_vote_result.vote_sequence)+u"轮 "+str(each_vote_result.civilian_vote_count)+u"："+\
                         str(each_vote_result.spy_vote_count)+u" "+winner_side+u"\n")
        
    return final_result
    
def formate_query_reply(civilian_winned,spy_winned,vote_result_list):
    current_result = queryReply %(civilian_winned,spy_winned)
    for each_vote_result in vote_result_list:
        winner_side = u"战"
        if each_vote_result.which_side_get_point == "spy":
            winner_side = u"谍"
        current_result += (str(each_vote_result.vote_sequence)+u"轮 "+str(each_vote_result.civilian_vote_count)+u"："+\
                         str(each_vote_result.spy_vote_count)+u" "+winner_side+u"\n")
        
    return current_result
    
    
def get_point_requirement(user_count):
    if user_count == 5:
        return u"1/2 1/3 1/2 1/3 1/3"
    elif user_count == 6:
        return u"1/2 1/3 1/4 1/3 1/4"
    elif user_count == 7 :
        return u"1/2 1/3 1/3 2/4 1/4"
    elif user_count == 8 or user_count == 9 or user_count == 10 or user_count == 11 or user_count == 12:
        return u"1/3 1/4 1/4 2/5 1/5"
        
        
        
