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
from Tools.unreal_tools import utils
imp.reload(addActor)
imp.reload(checkChangeList)

Tools = {
    "AddActor": {
        "type": "window",
        "name": "Add P4",
        "function": addActor.AddActor,
        "icon": os.path.join(os.path.dirname(__file__), "icons/getActor.png")
    },
    "CheckChange": {
        "type": "window",
        "name": "Get Actor",
        "function": checkChangeList.CheckChange,
        "icon": os.path.join(os.path.dirname(__file__), "icons/target.png")
    },
    "Help": {
        "type": "run",
        "name": "Help",
        "function": utils.openHelp,
        "icon": os.path.join(os.path.dirname(__file__), "icons/help.png")
    }
}
