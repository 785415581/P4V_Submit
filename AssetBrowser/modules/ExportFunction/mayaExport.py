# -*- coding: UTF-8 -*-
import pymel.core as pm
import maya.cmds as cmds
from ..global_setting import MAYALEVEL
class MayaExport():
    def __init__(self, step):
        self.log = ""
        self.result = ""
        self.publish_step = step

        #self.scene_check(step)

    def scene_check(self):
        self.check_hierarcy()
        self.log = u"Success:场景检查通过"
        self.result = True



    def check_hierarcy(self):
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
            self.log = u"Error:检查组{0}".format(export_level)
            self.result = False
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


        #todo waiting to judge if fbx export need change
        cmds.file(export_file, force=True, typ=file_type, pr=True, es=True)
        pm.select(clear=True)
        self.log = "Success!"
        self.result = True




