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
from AssetBrowser.utils.log import ToolsLogger
wx_bot = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d828bfd1-3f07-498e-aaed-e3d2bcf3a94e"
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def send_msg(**kwargs):
    notice = kwargs.get('notice', '')
    taskId = kwargs.get('taskID', '')
    taskId = taskId.replace('ID', '')
    taskStatus = kwargs.get('taskStatus', '')
    status = ""
    if taskStatus == u'未开始':
        status = '<font color=#8dc572>未开始</font>'
    elif taskStatus == '进行中':
        status = '<font color=#1d80f5>未开始</font>'
    elif taskStatus == '已完成':
        status = '<font color=#8b95a7>未开始</font>'
    dst_files = kwargs.get('dst_files', '')
    assetName = kwargs.get('assetName', '')
    assetStep = kwargs.get('assetStep', '')
    p4model = kwargs.get("p4model", "")
    fils = ''
    for file in dst_files:
        fils = fils + '\n' + os.path.basename(file)

    markdown_msg = "# {assetStep}艺术家 {userName} 提交了资产 <font color=#1766c4>{assetName}</font>\n" \
                   ">文件名称 : <font color=\"comment\">{fileName}</font>\n" \
                   ">提交人   : <font color=\"comment\">{userName}</font>\n" \
                   ">提交时间 : <font color=\"comment\">{time}</font>\n" \
                   ">下游人员 : <font color=#ff3c20>{noticeMember}</font>\n" \
                   ">任务 ID ：[{id}](https://www.tapd.cn/61223525/prong/tasks/view/116122352500{id})\n" \
                   ">任务状态 ：{status}".format(
                            assetName=assetName,
                            assetStep=assetStep,
                            userName=p4model.user.capitalize(),
                            fileName=fils,
                            time=now_time,
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
    requests.post(wx_bot, data_markdown, auth=('Content-Type', 'application/json'), verify=False)
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
    send_msg(assetName="TATest", assetStep="Rig", notice='刘雅旭;程缓缓;秦家鑫', taskID='1053143', dst_files=['SM_Football.fbx', 'SM_Football.fbx', 'SM_Football.fbx'])
    # noticeConfig = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'noticeConfig.json')
    # import base64
    # import pickle
    # with open(noticeConfig, 'r', encoding='utf-8') as fp:
    #     data = json.load(fp)
    # bytejson=pickle.dumps(data)
    # print(bytejson)