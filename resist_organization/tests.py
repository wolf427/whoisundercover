# -*- coding: utf-8 -*-
from django.test import TestCase
from wechat_sdk.basic import WechatBasic
from wechat_sdk.core.conf import WechatConf
from resist_organization.views import process_msg

signature = 'f24649c76c3f3d81b23c033da95a7a30cb7629cc' 
timestamp = '1406799650' 
nonce = '1505845280'
# Create your tests here.
body_text = """
<xml>
<ToUserName><![CDATA[touser]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>1405994593</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<MsgId>6038700799783131222</MsgId>
</xml>
"""
token='WECHAT_TOKEN'

def sendMsg(userName,content):
    msg = body_text %(userName,content) 
    wechat_instance = WechatBasic(token=token)
    if wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        wechat_instance.parse_data(msg)
        print process_msg(wechat_instance.get_message())