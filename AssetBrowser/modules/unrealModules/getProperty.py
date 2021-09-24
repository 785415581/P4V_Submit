#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/9/22 15:29
"""

import unreal


def getAllProperties(object_class):
    return unreal.CppLib.get_all_properties(object_class)

def printAllProperties():
obj = unreal.Actor()
object_class = obj.get_class()
for x in unreal.MyBlueprintFunctionLibraryTest.get_all_properties(object_class):
    print(x)
    y = x
    while len(y) < 50:
        y = ' ' + y
    print(y + ' : ' str(obj.get_editor_property(x)))

printAllProperties()