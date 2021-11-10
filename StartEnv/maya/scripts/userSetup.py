import sys
ToolLib = r"R:/ProjectX/Scripts/Python/tools/publish"

if ToolLib not in sys.path:
    sys.path.append(ToolLib)


def maya_main_window():
    from maya import OpenMayaUI
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def open_window(*args):
    import AssetBrowser.main as main
    import imp
    imp.reload(main)

    try:
        win.close()
        win.deleteLater()
    except:
        pass
    from PySide2.QtWidgets import QApplication
    for widget in QApplication.topLevelWidgets():
        if widget.objectName() == "PublishTools":
            widget.deleteLater()
    win = main.MainWindow(parent=maya_main_window())
    win.setObjectName('PublishTools')
    win.show()


def createLevel(*args):
    import Tools.maya.createHierarchy as createHierarchy
    createHierarchy.createHierarchy(asset=True)

import maya.cmds as cmds
if cmds.menu('AuroraTools', exists=1):
    cmds.deleteUI('AuroraTools')
showMyMenu = cmds.menu("AuroraTools", parent="MayaWindow", to=1, aob=1, label=u"JGTools")
cmds.menuItem(parent=showMyMenu, label='Publish', command=open_window)
cmds.menuItem(parent=showMyMenu, label='CreateHierarchy', command=createLevel)