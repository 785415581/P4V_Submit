
import AssetBrowser.modules.publish_hooks.moveFile as moveFile

import imp
imp.reload(moveFile)

def startPublish(item_files, basePublish):
    for item_file in item_files:
        ws_file = moveFile(item_file)
        log, res = basePublish.addChangeList(ws_file)
        if not res:
            return log, res
        log, res = basePublish.submit()
        if not res:
            return log, res




