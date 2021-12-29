#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/12/28 16:43
"""
import os
import imp
from Tools.unreal_tools import addActor
from Tools.unreal_tools import checkChangeList
imp.reload(addActor)
imp.reload(checkChangeList)

Tools = {
    "AddActor": {
        "name": "Add P4",
        "function": 'addActor.AddActor',
        "icon": os.path.join(os.path.dirname(__file__), "icons/getActor.png")
    },
    "CheckChange": {
        "name": "Get Actor",
        "function": checkChangeList.CheckChange,
        "icon": os.path.join(os.path.dirname(__file__), "icons/target.png")
    }
}
