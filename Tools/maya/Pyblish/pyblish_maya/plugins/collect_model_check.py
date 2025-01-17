import pyblish.api


class CollectMayaWorkspace(pyblish.api.ContextPlugin):
    """Inject the current workspace into context"""

    order = pyblish.api.CollectorOrder - 0.5
    label = "Maya Model"

    hosts = ['example']
    version = (0, 1, 0)

    def process(self, context):
        import os
        from maya import cmds

        workspace = cmds.workspace(rootDirectory=True, query=True)
        if not workspace:
            # Project has not been set. Files will
            # instead end up next to the working file.
            workspace = cmds.workspace(dir=True, query=True)

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(workspace)

        context.set_data('workspaceDir', value=normalised)

        # For backwards compatibility
        context.set_data('workspace_dir', value=normalised)