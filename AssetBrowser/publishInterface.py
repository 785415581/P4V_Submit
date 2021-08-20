import os
from AssetBrowser.utils import loader
from AssetBrowser.publish_hooks import basePublish


def get_step_interface_class(stepName=None):
    hookDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'publish_hooks')).replace('\\', '/')
    hookDefault = "%s/basePublish.py" % hookDir
    if stepName:
        hookName = "%s_interface.py" % stepName.lower()
        hookPath = "%s/%s" % (hookDir, hookName)
        if os.path.exists(hookPath):
            return loader.load_custom_module(hookPath, basePublish.BasePublish)
    return loader.load_custom_module(hookDefault, object)