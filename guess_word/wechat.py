# -*- coding: utf-8 -*-
'''
Created on 2016年3月19日

@author: wolf
'''
guess_word_reply = u"""猜的词语：%s
回复【换】更换词语"""

def formate_guess_reply(word_content):
    return guess_word_reply %(word_content)