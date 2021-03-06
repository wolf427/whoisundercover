# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseBadRequest


from wechat_sdk import WechatConf,WechatBasic
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from resist_organization.views import process_msg
from resist_organization import wechat

conf = WechatConf(
    token='wolf427', 
    appid='wx84482dcc4f137d43', 
    appsecret='434f96eaed9dac9aa79905e9d51618b3', 
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='rEMVGpxvdPcL3sItiqtWeb0e76j2iclL5WCBXM5017D'  # 如果传入此值则必须保证同时传入 token, appid
)

# Create your views here.
@csrf_exempt
def process(request):
    wechat_instance = WechatBasic(conf=conf)
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
 
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
 
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")
     
     # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body.decode('utf-8'))
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')
 
    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
 
    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content = (
            wechat.nothing_reply
            ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
#         if content == '功能':
#             reply_text = (
#                     '目前支持的功能：\n1. 关键词后面加上【教程】两个字可以搜索教程，'
#                     '比如回复 "Django 后台教程"\n'
#                     '2. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
#                     '还有更多功能正在开发中哦 ^_^\n'
#                     '【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
#                 )
#         elif content.endswith('教程'):
#             reply_text = '您要找的教程如下：'
        reply_text = process_msg(message)
        if reply_text == None:
            reply_text = wechat.nothing_reply
        response = wechat_instance.response_text(content=reply_text)
 
    return HttpResponse(response, content_type="application/xml")   
        
        
        
        
    