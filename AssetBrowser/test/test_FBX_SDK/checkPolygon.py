#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/30 11:48
"""
import fbx
import FbxCommon


def read_fbx_frame(fbx_file):
    # NOTE read FBX frame count
    manager, scene = FbxCommon.InitializeSdkObjects()
    # NOTE 只导入 Global_Settings 读取帧数
    s = manager.GetIOSettings()
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Material", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Texture", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Audio", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Audio", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Shape", False)
    s.SetBoolProp("Import|AdvOptGrp|FileFormat|Fbx|Link", False)
    s.SetBoolProp(fbx.EXP_FBX_GOBO, False)
    s.SetBoolProp(fbx.EXP_FBX_ANIMATION, False)
    s.SetBoolProp(fbx.EXP_FBX_CHARACTER, False)
    s.SetBoolProp(fbx.EXP_FBX_GLOBAL_SETTINGS, True)

    manager.SetIOSettings(s)

    result = FbxCommon.LoadScene(manager, scene, fbx_file)
    if not result:
        raise RuntimeError("%s load Fail" % fbx_file)

    setting = scene.GetGlobalSettings()
    time_span = setting.GetTimelineDefaultTimeSpan()
    time_mode = setting.GetTimeMode()
    frame_rate = fbx.FbxTime.GetFrameRate(time_mode)
    duration = time_span.GetDuration()
    second = duration.GetMilliSeconds()
    # NOTE unreal 计算第0帧 所以要 + 1 才和 unreal 的实际长度匹配
    frame_count = round(second/1000*frame_rate) + 1
    return frame_count

filePath = "D:/workSpace/Python/Tools/publish/AssetBrowser/test/test_FBX_SDK/myFbxSaveFile.fbx"

frame_count = read_fbx_frame(filePath)
print(frame_count)