# -*- coding: UTF-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import imp
from ..global_setting import MAYALEVEL, ANISTEP
import AssetBrowser.view.baseWidget as baseWidget
import AssetBrowser.modules.app_utils as app_utils
imp.reload(baseWidget)
imp.reload(app_utils)


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
        import maya.mel as mel
        if not pm.PyNode(export_level).listRelatives():
            self.log = u"组{0}为空".format(export_level)
            self.result = True
            return self.log, self.result

        if export_file.endswith(".ma"):
            file_type = "mayaAscii"
        elif export_file.endswith(".fbx"):
            file_type = "FBX export"
        else:
            self.log = u"Error:{0} 格式不支持导出".format(export_file.split(".")[-1])
            self.result = False
            return self.log, self.result
        pm.select(clear=True)
        pm.select(export_level)
        if export_file.endswith(".fbx"):
            cmds.FBXProperty('Export|IncludeGrp|Animation', '-v', 0)
            mel.eval("FBXExportSmoothingGroups -v 1")

        #todo waiting to judge if fbx export need change
        cmds.file(export_file, force=True, typ=file_type, pr=True, es=True)
        pm.select(clear=True)
        self.log = "Finish export...."
        self.result = True

    def export_rig(self, export_file, export_level):
        app_utils.add_log("Export Rig")
        import maya.mel as mel
        self.log = ""
        self.result = False

        self.log = ""
        self.result = False

        if export_file.endswith(".ma"):
            file_type = "mayaAscii"
        elif export_file.endswith(".fbx"):
            file_type = "FBX export"
        else:
            self.log = u"Error:{0} 格式不支持导出".format(export_file.split(".")[-1])
            self.result = False
            return

        jntList = []
        for child_level in cmds.listRelatives(export_level, allDescendents=True):
            try:
                skin = mel.eval("findRelatedSkinCluster " + child_level)
            except:
                continue

            if skin:
                jntList = pm.skinCluster(skin, q=1, wi=1)
                jnt = jntList[0]
                while True:
                    p1 = pm.listRelatives(jnt, parent=True, type='joint')
                    if p1:
                        jnt = p1[0]
                    else:
                        p1 = jnt
                        break
                pm.parent(jnt, w=1)
                break

        if not jntList:
            self.log = "No joint found"
            self.result = False
            return
        pm.select(clear=True)
        pm.select(export_level)
        pm.select(jnt, add=True)

        # set group save in .ma file
        cmds.select("Sets", add=1, ne=1)
        anils = [0, 'false', 0, 24]

        cmds.FBXProperty('Export|IncludeGrp|Animation', '-v', anils[0])
        mel.eval('FBXExportBakeComplexAnimation -v %s' % anils[1])
        mel.eval('FBXExportBakeComplexStart  -v %i' % anils[2])
        mel.eval('FBXExportBakeComplexEnd  -v %i' % anils[3])
        mel.eval('FBXExportBakeComplexStep  -v 1')
        mel.eval('FBXExportBakeResampleAnimation  -v false')
        mel.eval('FBXExportAnimationOnly  -v false ')
        mel.eval("FBXExportSmoothingGroups -v 1")


        cmds.file(export_file, force=True, options='v=0', type=file_type, pr=True, es=True)
        pm.select(clear=True)
        self.log = file_type
        self.result = True


    def export_ani(self, export_file, export_level):
        app_utils.add_log("Export Ani")
        import maya.mel as mel
        self.log = ""
        self.result = False

        self.log = ""
        self.result = False

        if export_file.endswith(".ma"):
            file_type = "mayaAscii"
        elif export_file.endswith(".fbx"):
            file_type = "FBX export"
        else:
            self.log = u"Error:{0} 格式不支持导出".format(export_file.split(".")[-1])
            self.result = False
            return

        jntList = []
        child_nodes = cmds.listRelatives(export_level, allDescendents=True)
        if not child_nodes:
            self.log = "Group {0} is null group".format(export_level)
            self.result = True
            return
        for child_level in child_nodes:
            try:

                skin = mel.eval("findRelatedSkinCluster " + child_level)
            except:
                continue

            if skin:
                jntList = pm.skinCluster(skin, q=1, wi=1)
                if not jntList:
                    self.log = "Failed {0} to find jnt"
                    self.result = False
                    return
                # pm.parent(jntList[0], w=1)
                break

        if not jntList:
            self.log = "No joint found"
            self.result = False
            return
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)
        anils = [1, 'true', start, end]

        cmds.FBXProperty('Export|IncludeGrp|Animation', '-v', anils[0])
        mel.eval('FBXExportBakeComplexAnimation -v %s' % anils[1])
        mel.eval('FBXExportBakeComplexStart  -v %i' % anils[2])
        mel.eval('FBXExportBakeComplexEnd  -v %i' % anils[3])
        mel.eval('FBXExportBakeComplexStep  -v 1')
        mel.eval('FBXExportBakeResampleAnimation  -v false')
        mel.eval('FBXExportAnimationOnly  -v false ')
        mel.eval("FBXExportSmoothingGroups -v 1")

        pm.select(clear=True)
        # pm.select(export_level)
        pm.select(jntList, add=True)

        cmds.file(export_file, force=True, options='v=0', type=file_type, pr=True, es=True)
        pm.select(clear=True)
        self.log = file_type
        self.result = True








