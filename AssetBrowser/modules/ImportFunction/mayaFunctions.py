import maya.cmds as cmds
import pymel.core as pm
import os


def createHierarchy(asset=False, shot=False):
    from Tools.maya.createHierarchy import createHierarchy
    createHierarchy(asset, shot)


def mayaImport(sel_file_list, type):
    for sel_file in sel_file_list:
        createNodes = cmds.file(sel_file, i=True, type=type, ignoreVersion=True, mergeNamespacesOnClash=True, namespace=':',
                            returnNewNodes=True)
        yield createNodes

def MayaImportMa(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    # createHierarchy()
    createNodes = mayaImport(sel_file_list, "mayaAscii")
    return "", createNodes

def MayaImportMb(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    createNodes = mayaImport(sel_file_list, "mayaBinary")
    return "", createNodes

def MayaImportFBX(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    createNodes = mayaImport(sel_file_list, "FBX")
    return "", createNodes

def MayaImportABC(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    if not cmds.pluginInfo("AbcImport.mll", l=True, q=True):
        cmds.loadPlugin("AbcImport.mll")
    #todo time range
    for sel_file in sel_file_list:
        cmds.AbcImport(sel_file, mode="import")


def MayaImportImage(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    file_name = os.path.basename(sel_file_list).split(".")[0]
    file_read = cmds.shadingNode("file", asTexture=True, isColorManaged=True, n=file_name)
    cmds.setAttr(file_read+"fileTextureName", sel_file_list, type="string")


def getNameSpace(sel_file):
    return os.path.basename(sel_file).split(".")[0]


def mayaReference(sel_file, file_type, namespace, **kwargs):
    model = None
    if kwargs["fileInfo"][sel_file]["step"] == "Rig":
        import AssetBrowser.view.widgetAniModel as widgetAniModel
        import imp
        imp.reload(widgetAniModel)
        modelWin = widgetAniModel.AniModelWidget()
        modelWin.exec_()
        model = modelWin.select_model
        modelWin.destroy()

    refe_return = cmds.file(sel_file, r=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
              namespace=namespace, returnNewNodes=True)
    if model:
        createHierarchy(shot=True)
        for create_node in refe_return:
            if create_node.endswith(":master"):
                asset_master_node = pm.PyNode(create_node)
                pm.parent(asset_master_node, "|ani|"+model)

    return "Reference: {0}".format(sel_file), True


def MayaReferenceMa(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    for sel_file in sel_file_list:
        ns = getNameSpace(sel_file)
        mayaReference(sel_file, "mayaAscii", ns, **kwargs)
    return "Reference: {0}".format(";".join(sel_file_list)), True


def MayaReferenceMb(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    for sel_file in sel_file_list:
        ns = getNameSpace(sel_file)
        mayaReference(sel_file, "mayaBinary", ns, **kwargs)
    return "Reference: {0}".format(";".join(sel_file_list)), True



def MayaReferenceFBX(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    for sel_file in sel_file_list:
        ns = getNameSpace(sel_file)
        mayaReference(sel_file, "FBX", ns, **kwargs)
    return "Reference: {0}".format(";".join(sel_file_list)), True



def MayaReferenceABC(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    for sel_file in sel_file_list:
        file_name = os.path.basename(sel_file).split(".")[0]
        gpu_in = pm.createNode("gpuCache", n=file_name+"Shape")
        gpu_in.parent(0).rename("test_gpu")
        gpu_in.setAttr("cacheFileName", sel_file, type="string")

    return "", True


def MayaOpen(sel_file, file_type, **kwargs):
    cmds.file(sel_file, o=True, f=True, ignoreVersion=True, type=file_type)
    # cmds.addRecentFile(sel_file, file_type)

    return "", True


def MayaOpenMa(**kwargs):
    sel_file_list = kwargs["fileInfo"].keys()
    for sel_file in sel_file_list:
        MayaOpen(sel_file, "mayaAscii")

    return "", True

