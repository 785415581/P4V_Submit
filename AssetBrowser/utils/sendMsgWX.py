#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/23 11:21
"""
import os
import re
import getpass

import requests, json
import datetime
import traceback
from AssetBrowser.utils.log import ToolsLogger
wx_bot = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d828bfd1-3f07-498e-aaed-e3d2bcf3a94e"
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

cwx_user = {"Chengyanfeng": "陈岩峰", "Duyunlong": "杜云龙", "Liuzhilei": "刘志磊", "Lixin": "李鑫", "Lvyan": "吕妍",
            "Minjie": "闵杰", "Peiyangyang": "裴阳阳", "Shenchuan": "申川", "Tengzhenyi": "滕哥", "Wangyuanhao": "王元昊",
            "Xuezherong": "薛哲荣", "Yanyubin": "严育斌", "Zhangxinlong": "张鑫龙"}


def send_msg(**kwargs):
    notice = kwargs.get('notice', '')
    if notice == "(无选择)":
        notice = ""
    des = kwargs.get('log', '')
    taskId = kwargs.get('taskID', '')
    taskId = taskId.replace('ID', '')
    taskStatus = kwargs.get('taskStatus', '')
    status = ""
    if taskStatus == u'未开始':
        status = '<font color=#8dc572>未开始</font>'
    elif taskStatus == '进行中':
        status = '<font color=#1d80f5>进行中</font>'
    elif taskStatus == '已完成':
        status = '<font color=#8b95a7>已完成</font>'
    dst_files = kwargs.get('dst_files', '')
    assetName = kwargs.get('assetName', '')
    assetStep = kwargs.get('assetStep', '')
    p4model = kwargs.get("p4model", "")
    userName = cwx_user.get(p4model.user.capitalize(), "")
    if not userName:
        userName = p4model.user.capitalize()
    fils = ''
    for file in dst_files:
        fils = fils + '\n' + os.path.basename(file)

    markdown_msg = "# {userName} 提交了资产 <font color=#1766c4>{assetName}</font>\n" \
                   ">文件名称 : <font color=\"comment\">{fileName}</font>\n" \
                   ">提交人   : <font color=\"comment\">{userName}</font>\n" \
                   ">提交环节 : <font color=\"comment\">{assetStep}</font>\n" \
                   ">提交时间 : <font color=\"comment\">{time}</font>\n" \
                   ">提交描述 : <font color=#ff3c20>{des}</font>\n" \
                   ">下游人员 : <font color=#ff3c20>{noticeMember}</font>\n" \
                   ">任务 ID ：[{id}](https://www.tapd.cn/61223525/prong/tasks/view/116122352500{id})\n" \
                   ">任务状态 ：{status}".format(
                            assetName=assetName,
                            assetStep=assetStep,
                            userName=userName,
                            fileName=fils,
                            time=now_time,
                            des=des,
                            noticeMember=notice,
                            id=taskId,
                            status=status
                        )


    data_markdown = json.dumps(
        {
            "msgtype": "markdown",
            "markdown":
                {
                    "content": markdown_msg,
                }
        }
    )

    data_text = json.dumps(
        {
            "msgtype": "text",
            "text": {
                "content": "",
                # "mentioned_list": ["wangqing", "@all"],
                # "mentioned_mobile_list": mentioned_list
            }
        }
    )

    requests.packages.urllib3.disable_warnings()
    proxies = {"http": None, "https": None}
    try:
        requests.post(wx_bot, data_markdown, auth=('Content-Type', 'application/json'), verify=False, proxies=proxies)
    except ConnectionError as e:
        error = traceback.print_exc()
        ToolsLogger.get_logger(error, save_log=True)
    # requests.post(wx_bot, data_text, auth=('Content-Type', 'application/json'), verify=False)


def updateTAPDTaskStatus(**kwargs):
    taskID = kwargs.get('taskID', '')
    taskStatus = kwargs.get('taskStatus', '')
    statusDic = {u"未开始": "open", u"进行中": "progressing", u"已完成": "done"}
    status = statusDic.get(taskStatus, '')
    if not taskID:
        return
    if not status:
        return
    api_user = 'gNxpkwrr'
    api_password = '86EE396F-6733-051C-3BA9-1243A2E8AA36'
    payload = {'workspace_id': '61223525', 'id': '116122352500{}'.format(taskID), 'status': status}
    try:
        r = requests.post("https://api.tapd.cn/tasks", data=payload, auth=(api_user, api_password))
        print(r.text)
    except ConnectionResetError as e:
        ToolsLogger.get_logger(e, save_log=True)


if __name__ == '__main__':
    # updateTAPDTaskStatus(taskID="1054299", taskStatus=u"进行中")

    send_msg(assetName="TATest", assetStep="Rig", notice='刘雅旭;程缓缓;秦家鑫', taskID='1053143', dst_files=['SM_Football.fbx', 'SM_Football.fbx', 'SM_Football.fbx'])
    # noticeConfig = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'noticeConfig.json')
    # import base64
    # import pickle
    # with open(noticeConfig, 'r', encoding='utf-8') as fp:
    #     data = json.load(fp)
    # bytejson=pickle.dumps(data)
    # print(bytejson)

    # from urllib import request
    # url = "https://www.tapd.cn/61223525/prong/{taskType}/view/116122352500{id}".format(taskType="stories", id='1053913')
    # print(url)
    # "https://www.tapd.cn/61223525/prong/stories/view/1161223525001053913"
    # "https://www.tapd.cn/61223525/prong/tasks/view/1161223525001051242"
    # from urllib import request
    #
    # with request.urlopen(url) as file:
    #     print(file.status)
    #     print(file.reason)
    # res = requests.get(url)
    # from pprint import pprint
    # pprint(res.text)
