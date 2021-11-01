
import AssetBrowser.modules.publish_hooks.basePublish as basePublish

import imp
imp.reload(basePublish)

def startPublish(item_files, **kwargs):
    basePublishInstance = basePublish.BasePublish()
    basePublishInstance.p4Model = kwargs["p4model"]


    log, res = basePublishInstance.checkout(item_files, publish_log=kwargs["log"])
    if not res:
        return log, res
    log, res = basePublishInstance.submit()
    return log, res



