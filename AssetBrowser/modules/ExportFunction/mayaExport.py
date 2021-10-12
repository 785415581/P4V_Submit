# -*- coding: UTF-8 -*-
import pyeml.core as pm

class MayaExport():
    def __init__(self, step):
        self.log = ""
        self.result = ""
        #self.scene_check(step)

    def scene_check(self, step):
        self.check_hierarcy(step)


    def check_hierarcy(self, step):
        hierarchy_level = {
            "rig": "|master",
            "Meshes": "|master",
            "Animations": "|ani|Textures"
        }
        self.root_node = hierarchy_level[step]
        if not pm.PyNode(self.root_node):
            self.log = u"Error:{0}不存在".format(self.root_node)


    def export_select(self, ext):
        if ext == "ma":
            pm.
