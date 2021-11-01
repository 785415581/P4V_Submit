import maya.cmds as cmds
import pymel.core as pm
import os


def createHierarchy(asset=False, shot=False):
    from Tools.maya.createHierarchy import createHierarchy
    createHierarchy(asset, shot)


def mayaImport(sel_file, type):

    cmds.file(sel_file, i=True, type=type, ignoreVersion=True, mergeNamespacesOnClash=True, namespace=':')


def MayaImportMa(sel_file, **kwargs):
    # createHierarchy()
    mayaImport(sel_file, "mayaAscii")
    return "", True

def MayaImportMb(sel_file, **kwargs):
    mayaImport(sel_file, "mayaBinary")
    return "", True

def MayaImportFBX(sel_file, **kwargs):
    mayaImport(sel_file, "FBX")
    return "", True

def MayaImportABC(sel_file, **kwargs):
    if not cmds.pluginInfo("AbcImport.mll", l=True, q=True):
        cmds.loadPlugin("AbcImport.mll")
    #todo time range
    cmds.AbcImport(sel_file, mode="import")

def MayaImportImage(sel_file, **kwargs):
    file_name = os.path.basename(sel_file).split(".")[0]
    file_read = cmds.shadingNode("file", asTexture=True, isColorManaged=True, n=file_name)
    cmds.setAttr(file_read+"fileTextureName", sel_file, type="string")


def getNameSpace(sel_file):
    return os.path.basename(sel_file).split(".")[0]


def mayaReference(sel_file, file_type, namespace, **kwargs):

    model = None
    if kwargs["step"] == "Rig":
        import AssetBrowser.view.aniModelWidget as aniModelWidget
        import imp
        imp.reload(aniModelWidget)
        modelWin = aniModelWidget.AniModelWidget()
        modelWin.exec_()
        model = modelWin.select_model
        modelWin.destroy()



    createHierarchy(shot=True)
    refe_return = cmds.file(sel_file, r=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
              namespace=namespace, returnNewNodes=True)
    if model:
        for create_node in refe_return:
            if create_node.endswith(":master"):
                asset_master_node = pm.PyNode(create_node)
                pm.parent(asset_master_node, "|ani|"+model)

    return "Reference: {0}".format(sel_file), True


def MayaReferenceMa(sel_file, **kwargs):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "mayaAscii", ns, **kwargs)


def MayaReferenceMb(sel_file, **kwargs):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "mayaBinary", ns, **kwargs)


def MayaReferenceFBX(sel_file,**kwargs):
    ns = getNameSpace(sel_file)
    return mayaReference(sel_file, "FBX", ns, **kwargs)


def MayaReferenceABC(sel_file, **kwargs):
    file_name = os.path.basename(sel_file).split(".")[0]
    gpu_in = pm.createNode("gpuCache", n=file_name+"Shape")
    gpu_in.parent(0).rename("test_gpu")
    gpu_in.setAttr("cacheFileName", sel_file, type="string")

    return "", True


def MayaOpen(sel_file, file_type, **kwargs):
    cmds.file(sel_file, o=True, f=True, ignoreVersion=True, type=file_type)
    # cmds.addRecentFile(sel_file, file_type)

    return "", True


def MayaOpenMa(sel_file, **kwargs):
    MayaOpen(sel_file, "mayaAscii")

    return "", True

