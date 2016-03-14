# -*- coding: utf-8 -*-
'''
Created on Mar 14, 2016

@author: yufeitan
'''
initRoomReply=u"""建房成功，请参与游戏人员直接输入房号【%d】加入游戏\n
                房号：  %d\n
                人数：  %d间谍  %d自由战士\n
                间谍：  %s\n
                """
joinRoomReply=u"""成功加入%d房间\n
                你的身份为%s\n
                你的号码为%d\n
        %s\n
                当你被选中投票时，直接回复【支持】（支持行动）或是【破坏】破坏行动
                """
                
voteReply=u"""
                第【%d】轮投票结束，投票结果：\n
                【%d】支持，【%d】破坏\n
                本轮任务：%s\n
                当前比分：%d：%d（战士：间谍）
"""
waitForInitRoomReply=u"""抵抗组织创建成功，请输入游戏人数【5-12】"""
gameOverReply=u"""
                游戏结束，%s胜利\n
                最终比分：%d：%d（战：谍）
                游戏过程如下：\n
                轮数 战：谍 得分\n
"""


def formatInitRoomReply(room):
    spiesCount = room.identityDistribution.split(",")
    return initRoomReply %(room.roomNum,room.roomNum,len(spiesCount),room.userCount-len(spiesCount)\
                           ,room.identityDistribution)
    
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
        final_result += (str(each_vote_result.vote_sequence)+u"轮"+str(each_vote_result.civilian_vote_count)+"："+\
                         str(each_vote_result.spy_vote_count)+" "+winner_side+"\n")
        
    return final_result
    
    
    
    
    
