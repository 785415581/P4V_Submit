import maya.cmds as cmds
import pymel.core as pm
import os

def createHierarchy(asset=False, shot=False):
    from Tools.maya.createhierarchy import createHierarchy
    createHierarchy(asset, shot)


def mayaImport(sel_file, type):

    cmds.file(sel_file, i=True, type=type, ignoreVersion=True, mergeNamespacesOnClash=True, namespace=':')


def MayaImportMa(sel_file, step):
    # createHierarchy()
    mayaImport(sel_file, "mayaAscii")

def MayaImportMb(sel_file, step):
    mayaImport(sel_file, "mayaBinary")

def MayaImportFBX(sel_file, step):
    mayaImport(sel_file, "FBX")

def MayaImportABC(sel_file, step):
    if not cmds.pluginInfo("AbcImport.mll", l=True, q=True):
        cmds.loadPlugin("AbcImport.mll")
    #todo time range
    cmds.AbcImport(sel_file, mode="import")

def MayaImportImage(sel_file, step):
    file_name = os.path.basename(sel_file).split(".")[0]
    file_read = cmds.shadingNode("file", asTexture=True, isColorManaged=True, n=file_name)
    cmds.setAttr(file_read+"fileTextureName", sel_file, type="string")


def getNameSpace(sel_file):
    return os.path.basename(sel_file).split(".")[0]


def mayaReference(sel_file, file_type, namespace, step=""):
    if step=="Rig":
        models = ["Idle", "Walk", "Run"]
        #todo one modle one file
        for model in models:
            model_ns = namespace+"_"+model
            createHierarchy(shot=True)
            cmds.file(sel_file, r=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
                      namespace=model_ns)
            asset_master_node = pm.PyNode(model_ns)
            pm.parent(asset_master_node, "|ani|"+model)

    createHierarchy(shot=True)
    cmds.file(sel_file, r=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
              namespace=namespace)
    if not pm.objExists(namespace+":"+"master"):
        return "Please check scene", False
    asset_master_node = pm.PyNode(namespace+":"+"master")
    pm.parent(asset_master_node, "|ani|rig")


def MayaReferenceMa(sel_file, step):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "mayaAscii", ns)


def MayaReferenceMb(sel_file, step):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "mayaBinary", ns)


def MayaReferenceFBX(sel_file, step):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "FBX", ns)


def MayaReferenceABC(sel_file, step):
    file_name = os.path.basename(sel_file).split(".")[0]
    gpu_in = pm.createNode("gpuCache", n=file_name+"Shape")
    gpu_in.parent(0).rename("test_gpu")
    gpu_in.setAttr("cacheFileName", sel_file, type="string")

    return "", True


def MayaOpen(sel_file, type):
    cmds.file(sel_file, o=True, f=True, ignoreVersion=True, type="mayaAscii")
    cmds.addRecentFile(sel_file, "mayaAscii")

    return "", True


def MayaOpenMa(sel_file, step):
    MayaOpen(sel_file, "mayaAscii")

    return "", True

