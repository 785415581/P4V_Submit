#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/24 18:22
"""

import requests
api_user = 'gNxpkwrr'
api_password = '86EE396F-6733-051C-3BA9-1243A2E8AA36'


def example():
    r = requests.get('https://api.tapd.cn/timesheets/entity_type=task&entity_id=1161223525001053143&owner=qinjiaxin&timespent=2&spentdate=2020-05-05&workspace_id=61223525', auth=(api_user, api_password))
    ret = r.json() # 获取接口返回结果

    from pprint import pprint
    pprint(ret)


def creatCategories():
    payload = {'workspace_id': '20480751', 'name': '简单用例目录'}
    r = requests.post("https://api.tapd.cn/tcase_categories", data=payload, auth=(api_user, api_password))
    print(r.text)


def creatTask():
    payload = {'workspace_id': '20480751', 'name': '简单用例', 'category_id': 1120480751001000463}
    r = requests.post("https://api.tapd.cn/tcases", data=payload, auth=(api_user, api_password))
    print(r.text)


def updateTask():
    payload = {'workspace_id': '61223525', 'id': '1161223525001053143', 'status': 'progressing'}
    r = requests.post("https://api.tapd.cn/tasks", data=payload, auth=(api_user, api_password))
    print(r.text)


def addComment():
    payload = {'workspace_id': '50616902', 'entry_id': '1150616902001054432', 'entry_type': 'tasks',
               'description': '12332455', 'author': '秦家鑫'}
    r = requests.post("https://api.tapd.cn/comments", data=payload, auth=(api_user, api_password))
    print(r.text)


if __name__ == '__main__':
    updateTask()