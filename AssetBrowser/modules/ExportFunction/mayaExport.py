# -*- coding: UTF-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import imp
from ..global_setting import MAYALEVEL, ANISTEP
import AssetBrowser.view.baseWidget as baseWidget
imp.reload(baseWidget)


class MayaExport():
    def __init__(self, step):
        self.log = ""
        self.result = ""
        self.publish_step = step

        #self.scene_check(step)

    def scene_check(self):
        self.check_hierarchy()
        self.log = u"Success:场景检查通过"
        self.result = True

    def unit_check(self):
        liner = cmds.currentUnit(query=True, linear=True)
        if liner != "cm":
            return False

    def check_hierarchy(self):
        #todo waiting to judge step name with s or not
        self.root_nodes = MAYALEVEL[self.publish_step]
        work_paths = MAYALEVEL[self.publish_step]["work"]
        exist = False
        has_child = False
        for work_path in work_paths:
            if pm.objExists(work_path):
                exist=True

            if pm.objExists(work_path) and pm.PyNode(work_path).listRelatives():
                has_child = True

        if (not exist) or (not has_child):

            self.log = u"Error:检查组{0}".format(";".join(work_paths))
            self.result = False
            return

    def export_publish_level(self, export_file, export_level):
        self.log = ""
        self.result = False
        if not pm.PyNode(export_level).listRelatives():
            self.log = u"组{0}为空".format(export_level)
            self.result = True
            return

        if export_file.endswith(".ma"):
            file_type = "mayaAscii"
        elif export_file.endswith(".fbx"):
            file_type = "FBX export"
        else:
            self.log = u"Error:{0} 格式不支持导出".format(export_file.split(".")[-1])
            self.result = False
            return
        pm.select(clear=True)
        pm.select(export_level)
        # baseWidget.LogPlainText().add_log(export_level, e=True)
        # baseWidget.LogPlainText().add_log(file_type, e=True)
        # baseWidget.LogPlainText().add_log("33333333333333", e=True)

        #todo waiting to judge if fbx export need change
        cmds.file(export_file, force=True, typ=file_type, pr=True, es=True)
        pm.select(clear=True)
        self.log = file_type
        self.result = True




