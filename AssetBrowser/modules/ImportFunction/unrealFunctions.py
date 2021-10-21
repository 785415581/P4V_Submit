#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/10/15 15:35
"""
import unreal


def UnrealImport():

    obj = UnrealObj()
    obj.type = "Character"
    obj.step = "Rig"
    obj.asset = "Cyber_Leopard"
    import_files = "C:/Dev/Assets/Character/Cyber_Leopard/Rig/Cyber_Leopard_rig.fbx"
    destination_path = obj.init_destination_path()
    destination_name = obj.init_destination_name()

    options = obj.build_static_mesh_import_options()
    importTask = obj.creatImportTask(import_files, destination_path, destination_name, options)
    obj.execute_import_tasks(importTask)


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
        return "/Game/{}/{}/{}".format(self.type, self.asset, self.step)

    def init_destination_name(self):
        return "SM_{}_{}".format(self.asset, self.step.upper())

    def build_static_mesh_import_options(self):
        """
        构建导入静态网格选项
        :return: options 导入静态网格选项
        """
        options = unreal.FbxImportUI()

        options.set_editor_property('import_mesh', True)
        options.set_editor_property("import_animations", False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', False)  # 是否当作骨骼物体来导入
        options.set_editor_property("import_textures", False)
        options.set_editor_property("import_rigid_mesh", False)
        options.set_editor_property("create_physics_asset", False)

        options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
        options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 0, 0))
        options.static_mesh_import_data.set_editor_property('import_uniform_scale', 10.0)

        options.static_mesh_import_data.set_editor_property('combine_meshes', True)
        options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
        options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)

        return options

    def creatImportTask(self, filename, destination_path, destination_name, options=None):
        """
            :param filename: 导入的文件的路径  eg: 'F:/workPlace/Scripts/MyTexture.TGA'
            :param destination_path: 导出后置产要放在什么位置 eg: '/GAME/Texture'
            :param options: 导入置产属性，     静态属性可由函数build_static_mesh_import_options获得，
                                        骨骼属性可由build_skeletal_mesh_import_options获得
            :return: Task 返回一个导入任务
        """
        importTask = unreal.AssetImportTask()
        importTask.set_editor_property("automated", True)
        importTask.set_editor_property('destination_name', destination_name)
        importTask.set_editor_property('destination_path', destination_path)
        importTask.set_editor_property('filename', filename)
        importTask.set_editor_property('replace_existing', True)
        importTask.set_editor_property('replace_existing_settings', True)
        importTask.set_editor_property('options', options)
        importTask.set_editor_property('save', True)

        return importTask

    def execute_import_tasks(self, tasks):
        """
        执行导入任务
        :param tasks: array 任务池
        :return: True
        """
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()  # 创建一个资产工具
        asset_tools.import_asset_tasks([tasks])  # 导入资产



# class UnrealImport:
#     def __init__(self, importFile, **kwargs):
#         super(UnrealImport, self).__init__()
#         self.importFile = importFile
#         self.kwargs = kwargs
#         self._type = None
#         self._asset = None
#         self._step = None
#
#     @property
#     def type(self):
#         return self._type
#
#     @type.setter
#     def type(self, value):
#         self._type = value
#
#     @property
#     def asset(self):
#         return self._asset
#
#     @asset.setter
#     def asset(self, value):
#         self._asset = value
#
#     @property
#     def step(self):
#         return self._step
#
#     @step.setter
#     def step(self, value):
#         self._step = value
#
#     def init_destination_path(self):
#         return "/Game/{}/{}/{}".format(self.type, self.asset, self.step)
#
#     def init_destination_name(self):
#         return "SM_{}_{}".format(self.asset, self.step.upper())
#
#     def build_static_mesh_import_options(self):
#         """
#         构建导入静态网格选项
#         :return: options 导入静态网格选项
#         """
#         options = unreal.FbxImportUI()
#
#         options.set_editor_property('import_mesh', True)
#         options.set_editor_property("import_animations", False)
#         options.set_editor_property('import_materials', False)
#         options.set_editor_property('import_as_skeletal', False)  # 是否当作骨骼物体来导入
#         options.set_editor_property("import_textures", False)
#         options.set_editor_property("import_rigid_mesh", False)
#         options.set_editor_property("create_physics_asset", False)
#
#         options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
#         options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 0, 0))
#         options.static_mesh_import_data.set_editor_property('import_uniform_scale', 10.0)
#
#         options.static_mesh_import_data.set_editor_property('combine_meshes', True)
#         options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
#         options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
#
#         return options
#
#     def creatImportTask(self, filename, destination_path, destination_name ,options=None):
#
#
#
#         return importTask
#
#     def execute_import_tasks(self, filename, destination_path, destination_name, options=None):
#         """
#             :param destination_name:
#             :param filename: 导入的文件的路径  eg: 'F:/workPlace/Scripts/MyTexture.TGA'
#             :param destination_path: 导出后置产要放在什么位置 eg: '/GAME/Texture'
#             :param options: 导入置产属性，     静态属性可由函数build_static_mesh_import_options获得，
#                                         骨骼属性可由build_skeletal_mesh_import_options获得
#             :return: Task 返回一个导入任务
#         """
#
#         importTask = unreal.AssetImportTask()
#         importTask.set_editor_property("automated", True)
#         importTask.set_editor_property('destination_name', destination_name)
#         importTask.set_editor_property('destination_path', destination_path)
#         importTask.set_editor_property('filename', filename)
#         importTask.set_editor_property('replace_existing', True)
#         importTask.set_editor_property('replace_existing_settings', True)
#         importTask.set_editor_property('options', options)
#         importTask.set_editor_property('save', True)
#
#         asset_tools = unreal.AssetToolsHelpers.get_asset_tools()  # 创建一个资产工具
#         asset_tools.import_asset_tasks([importTask])  # 导入资产
#
#
# select_file = "C:/Dev/Assets/Character/Cyber_Leopard/Rig/Cyber_Leopard_rig.fbx"
# info = {"type": "Character", "step": "Rig", "asset": "Cyber_Leopard"}
# obj = UnrealImport(select_file, info)
# # obj.type = "Character"
# # obj.step = "Rig"
# # obj.asset = "Cyber_Leopard"
# # import_files = "C:/Dev/Assets/Character/Cyber_Leopard/Rig/Cyber_Leopard_rig.fbx"
# # destination_path = obj.init_destination_path()
# # destination_name = obj.init_destination_name()
# #
# #
# # options = obj.build_static_mesh_import_options()
# # importTask = obj.creatImportTask(select_file, destination_path, destination_name, options)
# # obj.execute_import_tasks(importTask)
