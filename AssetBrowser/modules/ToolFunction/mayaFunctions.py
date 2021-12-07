import maya.cmds as cmds
import pymel.core as pm
import os
import imp
import AssetBrowser.modules.app_utils as app_utils
imp.reload(app_utils)
from AssetBrowser.modules.global_setting import ANISTEP


def mayaNew(**kwargs):
    from Tools.maya.createHierarchy import createHierarchy


    private_fold = kwargs["localPreWork"]
    private_fold = os.path.join(private_fold, "maya")
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)
    file_name = "{0}_{1}_v001.ma".format(kwargs["asset"].replace("/", "_"), kwargs["step"])
    work_file_path = os.path.join(private_fold, file_name)
    cmds.file(f=1, new=1)

    if kwargs["step"] == ANISTEP:
        createHierarchy(shot=True)
    else:
        createHierarchy(asset=True)

    cmds.file(rename=work_file_path)
    cmds.file(save=True, type='mayaAscii')
    return "Create New file:{0}".format(work_file_path), True


def mayaSave(**kwargs):
    import glob
    private_fold = os.path.join(kwargs["localPrePrivate"], "maya")
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)
    if kwargs["step"] == ANISTEP:
        for i in cmds.listRelatives("|ani", children=True):
            file_pre = "{0}_{1}_v".format(kwargs["asset"].replace("/", "_"), i)
            break
    else:
        file_pre = "{0}_{1}_v".format(kwargs["asset"].replace("/", "_"), kwargs["step"])
    file_name = file_pre + "*.ma"
    work_file_path = os.path.join(private_fold, file_name)
    version_list = glob.glob(work_file_path)
    if version_list:
        version_list.sort()
        last_version = version_list[-1]
        version_num = os.path.basename(last_version).split(".ma")[0].split(file_pre)[-1]
        new_version = str(int(version_num)+1).zfill(3)
    else:
        new_version = "001"

    file_name = file_pre + new_version + ".ma"
    work_file_path = os.path.join(private_fold, file_name)

    cmds.file(rename=work_file_path)
    cmds.file(save=True, type='mayaAscii')

    return "Save File {0}".format(work_file_path), True


def mayaImportSubAssets(**kwargs):
    import pymel.core as pm
    from Tools.maya.createHierarchy import createHierarchy
    from AssetBrowser.modules.global_setting import ANISTEP
    if kwargs["step"] == ANISTEP:
        createHierarchy(shot=True)
    else:
        createHierarchy(asset=True)

    import AssetBrowser.modules.ImportFunction.startImport as startImport
    import imp
    imp.reload(startImport)

    subAssetDict = kwargs["subAssets"]
    if kwargs["type"] not in subAssetDict:
        return "Type {0} has not subAssets".format(kwargs["type"]), False
    if kwargs["asset"] not in subAssetDict[kwargs["type"]]:
        return "Asset {0} has not subAssets".format(kwargs["asset"]), False
    subassets = subAssetDict[kwargs["type"]][kwargs["asset"]]

    for subasset in subassets:
        data_key = "{0}_{1}_{2}".format(kwargs["type"], subasset, kwargs["step"])
        if data_key not in kwargs["full_path_dict"]:
            app_utils.add_log("Subasset {0} Lack File".format(data_key), error=True)
            continue

        asset_files = kwargs["full_path_dict"][data_key]
        asset_level = "/{0}/".format(kwargs["asset"])
        subasset_level = "/{0}/".format(subasset)
        
        server_pre = kwargs["servePrePublish"].replace(asset_level, subasset_level)
        local_pre = kwargs["localPrePublish"].replace(asset_level, subasset_level)

        fileExt = list()
        fileInfo = {}

        for asset_file in asset_files:
            if not asset_file.endswith(".fbx"):
                continue
            # sync local version first
            kwargs["p4model"].syncFile(asset_file, version="head")
            asset_file = asset_file.replace(server_pre, local_pre)
            fileLabel = kwargs["p4model"].getFileLabels(asset_file)

            fileInfo[asset_file] = {}
            fileInfo[asset_file]['localPath'] = asset_file
            fileInfo[asset_file]['serverPath'] = asset_file.replace(local_pre, server_pre)
            fileInfo[asset_file]['type'] = kwargs["type"]
            fileInfo[asset_file]['asset'] = kwargs["asset"]
            fileInfo[asset_file]['step'] = kwargs["step"]
            fileInfo[asset_file]['labels'] = fileLabel
            fileInfo[asset_file]['ext'] = asset_file.split('.')[-1]
            fileExt.append(asset_file.split('.')[-1])


        fileExt = fileExt[0]
        import time
        log, create_nodes_yield = startImport.start_import("import", fileInfo=fileInfo, ext=fileExt)

        for create_nodes in create_nodes_yield:
            pass
            # for create_node in create_nodes:
            #     sub_level = "|master|" + kwargs["step"] + "|" + subasset.split("/")[-1]
            #     if not pm.objExists(sub_level):
            #         trans_node = pm.createNode("transform", n=subasset.split("/")[-1],
            #                                    p="|master|" + kwargs["step"])
            #     if "|master" in create_node and len(create_node.split("|")) < 5 and create_node != sub_level:
            #         pm.parent(pm.PyNode(create_node), trans_node)

    return "", True


def mayaExportSubAssets(**kwargs):
    import tempfile
    import imp
    import AssetBrowser.modules.ExportFunction.startExport as startExport
    import AssetBrowser.utils.utils as utils
    imp.reload(startExport)

    import AssetBrowser.view.widgetStep as widgetStep
    imp.reload(widgetStep)
    step_win = widgetStep.StepWidget(kwargs["step"])
    step_win.exec_()
    kwargs["step"] = step_win.select_step if step_win.select_step else kwargs["step"]
    index = kwargs["view"].submitStepCom.findText(kwargs["step"])
    kwargs["view"].submitStepCom.setCurrentIndex(index)
    step_win.destroy()

    scene_subassets = []
    if kwargs["type"] not in kwargs["subAssets"]:
        return "Failed to get subassets {0}".format(kwargs["asset"]), False

    if kwargs["step"] in ["Mesh", "Rig", "StaticMesh"]:
        transforms = []
        for outline_name in pm.listRelatives("|master|Mesh", children=True, ad=True, type="mesh"):
            transform_node = outline_name.parent(0)
            if transform_node.fullPath() in transforms:
                continue
            node_name = transform_node.name()
            node_name = node_name.split("|")[-1]
            subasset_name = kwargs["asset"] + "/" + node_name

            scene_subassets.append(subasset_name)
            transforms.append(transform_node.fullPath())
            kwargs["subAssets"][kwargs["type"]].setdefault(kwargs["asset"], set()).add(subasset_name)

    if not scene_subassets:
            return "Failed to get subassets {0}".format(kwargs["asset"]), False

    export_fold = utils.Utils.createPublishTemp()

    for subasset in scene_subassets:
        subasset_fold = export_fold + "/"+ subasset
        if not os.path.exists(subasset_fold):
            os.makedirs(subasset_fold)

        kwargs["asset"] = subasset
        log, result = startExport.start_export(subasset_fold, repalce_level=transforms[scene_subassets.index(subasset)], **kwargs)
        app_utils.add_log(log)
        if not result:
            print(subasset, log)
            os.rmdir(subasset_fold)

    for sub in os.listdir(export_fold):
        kwargs["view"].listWidget.createItem(os.path.join(export_fold, sub), source_model="export")


    return "", True








