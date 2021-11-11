
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
    if "sub_level" in kwargs:
        if "|" not in kwargs["sub_level"]:
            export_level = export_level + "|" + kwargs["sub_level"]
        else:
            export_level = export_level + kwargs["sub_level"]
    me.export_rig(export_file, export_level)

    return me.log, me.result


def ani_export(export_file, export_level, **kwargs):
    me = mayaExport.MayaExport(kwargs["step"])
    me.scene_check()
    if not me.result:
        return me.log, me.result

    if "sub_level" in kwargs:
        if "|" not in kwargs["sub_level"]:
            export_level = export_level + "|" + kwargs["sub_level"]
        else:
            export_level = export_level + kwargs["sub_level"]

    me.export_ani(export_file, export_level)

    return me.log, me.result





