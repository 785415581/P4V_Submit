
import AssetBrowser.modules.ExportFunction.mayaExport as mayaExport
import imp
imp.reload(mayaExport)


def default_export(export_file, export_level, **kwargs):
    me = mayaExport.MayaExport(kwargs["step"])
    me.scene_check()
    if not me.result:
        return me.log, me.result

    if "sub_level" in kwargs:
        if "|" not in kwargs["sub_level"]:
            export_level = export_level + "|" + kwargs["sub_level"]
        else:
            export_level = export_level + kwargs["sub_level"]

    me.export_publish_level(export_file, export_level)

    return me.log, me.result


def rig_export(export_file, export_level, **kwargs):
    me = mayaExport.MayaExport(kwargs["step"])
    me.scene_check()
    if not me.result:
        return me.log, me.result
    if "repalce_level" in kwargs:
        export_level = kwargs["repalce_level"]

    elif "sub_level" in kwargs:
        if "|" not in kwargs["sub_level"]:
            export_level = export_level + "|" + kwargs["sub_level"]
        else:
            export_level = export_level + kwargs["sub_level"]

    me.export_rig(export_file, export_level)

    return me.log, me.result


def ani_export(export_file, export_level, **kwargs):
    import maya.cmds as cmds
    me = mayaExport.MayaExport(kwargs["step"])
    for outline_name in cmds.listRelatives("|ani", children=True):
        sub_file = export_file.replace("model", outline_name)
        sub_level = export_level.replace("model", outline_name)
        if "sub_level" in kwargs:
            if "|" not in kwargs["sub_level"]:
                sub_level = sub_level + "|" + kwargs["sub_level"]
            else:
                sub_level = sub_level + kwargs["sub_level"]

        me.export_ani(sub_file, sub_level)

    #
    # me.scene_check()
    # if not me.result:
    #     return me.log, me.result





    return me.log, me.result





