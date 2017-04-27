#coding=utf8
import requests
import itchat
from random import choice

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text') + "\n-------by:Bruce Weifeng"
    except:
        return

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    if msg['Text'] == "傻逼" or msg['Text'] == "傻吊" or msg['Text'] == "狗屎" or msg['Text'] == "傻屌" or msg['Text'] == "二逼" or msg['Text'] == "费列罗":
        list = [
            "Fuck you the fucking fucker！",
            "Get the fucking my way！",
            "You're fucking piece of shit！",
            "your mother fucking bull shit ！",
            "I hate you! ",
            "You stupid jerk! ",
            "You bastard! ",
            "What a stupid idiot! ",
        ]
        return choice(list) + "\n-------by:Bruce Weifeng"
    else:
        defaultReply = 'I received: ' + msg['Text']
        reply = get_response(msg['Text'])
        return reply or defaultReply

itchat.auto_login(hotReload=True)
itchat.run()
