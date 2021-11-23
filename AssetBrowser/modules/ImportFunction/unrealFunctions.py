#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/10/15 15:35
"""
import unreal
import os
import sys
import json
import copy
import random
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from AssetBrowser.modules.extension import DialogAddLabel
import imp

imp.reload(DialogAddLabel)


def UnrealImportFBX(**kwargs):
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon("icon.png"))
    global window
    kwargs.update({"obj": FBXUnrealObj()})
    fileInfo = kwargs.get('fileInfo')
    window = DialogAddLabel.AddLabels()
    window.setWindowModality(QtCore.Qt.ApplicationModal)
    window.selectFiles = fileInfo
    window.kwargs = kwargs
    window.initUI()
    window.addFileItem(fileInfo)
    window.show()
    unreal.parent_external_window_to_slate(window.winId())
    return "", ""


def UnrealImportTex(**kwargs):
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon("icon.png"))
    global window
    kwargs.update({"obj": TexUnrealObj()})
    fileInfo = kwargs.get('fileInfo')
    window = DialogAddLabel.AddLabels()
    window.setWindowModality(QtCore.Qt.ApplicationModal)
    window.selectFiles = fileInfo
    window.kwargs = kwargs
    window.initUI()
    window.addFileItem(fileInfo)
    window.show()
    unreal.parent_external_window_to_slate(window.winId())
    return "", ""


class UnrealObj:
    def __init__(self):
        super(UnrealObj, self).__init__()
        self._type = None
        self._asset = None
        self._step = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        self._asset = value

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    def init_destination_path(self):
        pass

    def init_destination_name(self):
        pass

    def creatImportTask(self, filename, destination_path, destination_name, options=None):
        pass

    def execute_import_tasks(self, tasks):
        pass


class FBXUnrealObj(UnrealObj):
    def __init__(self):
        super(FBXUnrealObj, self).__init__()

    def init_destination_path(self, default=None):
        if default:
            return default
        return "/Game/{}/{}/{}".format(self.type, self.asset, self.step)

    def init_destination_name(self, default=None):
        if default:
            return default
        if self.step == 'Rig':
            return "SM_{}".format(self.step.upper())
        return "SM_{}".format(self.step.upper())

    def build_static_mesh_import_options(self):
        """
        构建导入静态网格选项
        :return: options 导入静态网格选项
        """
        options = unreal.FbxImportUI()

        # options.set_editor_property('import_mesh', True)
        # options.set_editor_property("import_animations", True)
        # options.set_editor_property('import_materials', False)
        # options.set_editor_property('import_as_skeletal', False)  # 是否当作骨骼物体来导入
        # options.set_editor_property("import_textures", False)
        # options.set_editor_property("import_rigid_mesh", False)
        # options.set_editor_property("create_physics_asset", False)

        # options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
        # options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 0, 0))
        # options.static_mesh_import_data.set_editor_property('import_uniform_scale', 10.0)
        #
        # options.static_mesh_import_data.set_editor_property('combine_meshes', True)
        # options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
        # options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)

        return options

    def creatImportTask(self, filePath, destination_path, destination_name, options=None):
        """
            :param destination_name:
            :param filename: 导入的文件的信息  g: kwargs
            :param destination_path: 导出后置产要放在什么位置 eg: '/GAME/Texture'
            :param options: 导入置产属性，     静态属性可由函数build_static_mesh_import_options获得，
                                        骨骼属性可由build_skeletal_mesh_import_options获得
            :return: Task 返回一个导入任务
        """
        taskList = list()

        importTask = unreal.AssetImportTask()
        importTask.set_editor_property("automated", False)
        # importTask.set_editor_property('destination_name', destination_name)
        importTask.set_editor_property('destination_path', destination_path)
        importTask.set_editor_property('filename', filePath)
        importTask.set_editor_property('replace_existing', True)
        importTask.set_editor_property('replace_existing_settings', True)
        importTask.set_editor_property('options', options)
        importTask.set_editor_property('save', True)
        taskList.append(importTask)
        return taskList

    def execute_import_tasks(self, tasks):
        """
        执行导入任务
        :param tasks: array 任务池
        :return: True
        """
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()  # 创建一个资产工具
        asset_tools.import_asset_tasks(tasks)  # 导入资产


class TexUnrealObj(UnrealObj):
    def __init__(self):
        super(TexUnrealObj, self).__init__()

    def init_destination_path(self, default=None):
        if default:
            return default
        return "/Game/{}/{}/{}".format(self.type, self.asset, self.step)

    def init_destination_name(self, default=None):
        if default:
            return default
        return "TX_{}".format(self.step.upper())

    def build_static_mesh_import_options(self):
        return None

    def creatImportTask(self, filePath, destination_path, destination_name, options=None):
        taskList = list()
        importTask = unreal.AssetImportTask()
        importTask.set_editor_property('filename', filePath)
        importTask.set_editor_property("automated", True)
        importTask.set_editor_property('destination_path', destination_path)
        # importTask.set_editor_property('destination_name', destination_name)
        importTask.set_editor_property('replace_existing_settings', True)
        importTask.set_editor_property('replace_existing', True)
        importTask.set_editor_property('options', options)
        importTask.set_editor_property('save', True)
        taskList.append(importTask)
        return taskList

    def execute_import_tasks(self, tasks):
        """
        执行导入任务
        :param tasks: array 任务池
        :return: True
        """
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()  # 创建一个资产工具
        asset_tools.import_asset_tasks(tasks)  # 导入资产


