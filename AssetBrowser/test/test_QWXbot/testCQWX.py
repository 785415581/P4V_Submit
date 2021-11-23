#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/19 16:12
"""
import requests


corpid = 'ww8fe691a21dcf15ae'
corpsecret = 'IXDM1OJGwzT_Qwm2XAetogczUVKgYcKTm5tDEiWniMI'
agentid = '1000137'


def getToken():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    response = requests.get(url)
    return response.json().get("access_token")


def sendMessage():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + getToken()
    data = {
           "touser": "15188221619",
           "msgtype" : "text",
           "agentid" : 1,
           "text" : {
               "content" : "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
           },
           "safe":0,
           "enable_id_trans": 0,
           "enable_duplicate_check": 0,
           "duplicate_check_interval": 1800
        }
    response = requests.post(url, {}, auth=('Content-Type', 'application/json'))
    print(response.text)


if __name__ == '__main__':
    sendMessage()