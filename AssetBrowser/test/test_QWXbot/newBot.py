#! -*- coding: utf-8 -*-

import requests, json
import datetime
import time

wx_bot = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d828bfd1-3f07-498e-aaed-e3d2bcf3a94e"
send_message = "测试：测试机器人1号………………………………！"


def get_current_time():
    """获取当前时间，当前时分秒"""
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.now().strftime("%H")
    mm = datetime.datetime.now().strftime("%M")
    ss = datetime.datetime.now().strftime("%S")
    return now_time, hour, mm, ss


def sleep_time(hour, m, sec):
    """返回总共秒数"""
    return hour * 3600 + m * 60 + sec


def send_msg():

    markdown_msg = "# <font color=#2b2b2b>{userName}</font>提交了一个资产，请相关同事注意。\n" \
                   ">文件名称 : <font color=\"comment\">{fileName}</font>\n" \
                   ">文件类型 : <font color=\"comment\">{fileType}</font>\n" \
                   ">任务状态 : <font color=\"comment\">{status}</font>\n" \
                   ">提交人   : <font color=\"comment\">{userName}</font>\n" \
                   ">任务 ID  ：[ID{id}](https://www.tapd.cn/61223525/prong/stories/view/116122352500{id})".format(
                            userName="秦家鑫",
                            fileName="SM_Football.fbx",
                            fileType="FBX",
                            status="Progress",
                            id="1053820"
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
                "mentioned_mobile_list": ["15188221619"]
            }
        }
    )
    requests.packages.urllib3.disable_warnings()
    requests.post(wx_bot, data_text, auth=('Content-Type', 'application/json'), verify=False)
    requests.post(wx_bot, data_markdown, auth=('Content-Type', 'application/json'), verify=False)



if __name__ == '__main__':
    send_msg()