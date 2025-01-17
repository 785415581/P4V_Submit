import pyblish.api


class CollectMayaCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""

    order = pyblish.api.CollectorOrder - 0.5
    label = "Maya Current File"

    hosts = ['example']
    version = (0, 1, 0)

    def process(self, context):
        import os
        from maya import cmds

        """Inject the current working file"""
        current_file = cmds.file(sceneName=True, query=True)
        if current_file:
            # Maya returns forward-slashes by default
            current_file = os.path.normpath(current_file)

        context.set_data('currentFile', value=current_file)

        # For backwards compatibility
        context.set_data('current_file', value=current_file)
