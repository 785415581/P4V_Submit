
from .mayaExport import MayaExport


def default_export(export_file, export_level, step):
    me = MayaExport(step)
    me.scene_check()
    if not me.result:
        return me.log, me.result
    me.export_publish_level(export_file, export_level)

    return me.log, me.result



