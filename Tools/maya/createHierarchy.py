
import pymel.core as pm

from AssetBrowser.modules.global_setting import MAYALEVEL


def createTransform(work_level):

    compents = work_level.split("|")
    for index in range(1, len(compents)):
        path = "|".join(compents[:(index+1)])
        if not pm.objExists(path):
            if index==1:
                trans_node = pm.createNode("transform", n=compents[index])
            else:
                trans_node = pm.createNode("transform", n=compents[index], p=pm.PyNode("|".join(compents[:index])))


def createHierarchy(asset=False, shot=False):
    if asset:
        hierarchy_type = "asset"
    if shot:
        hierarchy_type = "shot"
    for step, values in MAYALEVEL.items():

        if (values["type"] != hierarchy_type):
            continue

        for work_level in values["work"]:
            createTransform(work_level)