
import AssetBrowser.modules.ExportFunction.mayaExport as mayaExport
import imp
imp.reload(mayaExport)


def default_export(export_file, export_level, step):
    me = mayaExport.MayaExport(step)
    me.scene_check()
    if not me.result:

        return me.log, me.result
    me.export_publish_level(export_file, export_level)

    return me.log, me.result


def ani_export(export_file, export_level, step):
    me = mayaExport.MayaExport(step)
    me.scene_check()
    if not me.result:
        return me.log, me.result

    me.export_publish_level(export_file, export_level)





