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
from Tools.unreal_tools import GetActorBounding
from Tools.unreal_tools import GetAsset
from Tools.unreal_tools import ExcuteBlueprintWidget
from Tools.unreal_tools import utils
imp.reload(addActor)
imp.reload(checkChangeList)

Tools = {
    # "AddActor": {
    #     "type": "window",
    #     "name": "Add P4",
    #     "function": addActor.AddActor,
    #     "icon": os.path.join(os.path.dirname(__file__), "icons/getActor.png")
    # },
    "CheckChange": {
        "type": "window",
        "name": "Get Actor",
        "function": checkChangeList.CheckChange,
        "icon": os.path.join(os.path.dirname(__file__), "icons/target.png")
    },
    "ActorMainWindow": {
        "type": "window",
        "name": "Actor bounding box size",
        "function": GetActorBounding.ActorMainWindow,
        "icon": os.path.join(os.path.dirname(__file__), "icons/target.png")
    },
    "CheckAssets": {
        "type": "window",
        "name": "get asset",
        "function": GetAsset.MainWindow,
        "icon": os.path.join(os.path.dirname(__file__), "icons/search.png")
    },

    "BP_SortAsset": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/BP_SortAsset.BP_SortAsset",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "BP_CheckAsset": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/BP_CheckAsset.BP_CheckAsset",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_GetAllTexture": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_GetAllTexture.EUW_GetAllTexture",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_GoodsReplace": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_GoodsReplace.EUW_GoodsReplace",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_HLODLayerChecker": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_HLODLayerChecker.EUW_HLODLayerChecker",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_IntegrateInstances": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_IntegrateInstances.EUW_IntegrateInstances",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_LayerMaterialChecker": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_LayerMaterialChecker.EUW_LayerMaterialChecker",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_MergeSplineMesh": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_MergeSplineMesh.EUW_MergeSplineMesh",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },


    "EUW_PhysicalMaterialChecker": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_PhysicalMaterialChecker.EUW_PhysicalMaterialChecker",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_ResaveAssets": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_ResaveAssets.EUW_ResaveAssets",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "EUW_RuntimeGridChecker": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/EUW_RuntimeGridChecker.EUW_RuntimeGridChecker",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "ExtractBlueprint": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/ExtractBlueprint.ExtractBlueprint",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "FindBoundingBox": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/FindBoundingBox.FindBoundingBox",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },


    "FindExternalActors": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/FindExternalActors.FindExternalActors",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "InstancedFoliageActorChecker": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/InstancedFoliageActorChecker.InstancedFoliageActorChecker",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "InstancedFoliageActorManage": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/InstancedFoliageActorManage.InstancedFoliageActorManage",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "SetMeshPlatformsLOD": {
        "type": "run",
        "name": "Check Texture",
        "args": "/Game/Debug/Utilities/SetMeshPlatformsLOD.SetMeshPlatformsLOD",
        "function": ExcuteBlueprintWidget.ExcuteUtilityWidget,
        "icon": os.path.join(os.path.dirname(__file__), "icons/CheckTextureAlpha.png")
    },

    "Help": {
        "type": "run",
        "name": u"使用文档",
        "function": utils.openHelp,
        "icon": os.path.join(os.path.dirname(__file__), "icons/help.png")
    }
}
