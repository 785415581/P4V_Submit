import sys
ToolLib = r"R:/ProjectX/Scripts/Python/tools/publish"
import maya.cmds as cmds

if ToolLib not in sys.path:
    sys.path.insert(0, ToolLib)


def maya_main_window():
    from maya import OpenMayaUI
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def open_window(*args):

    from PySide2.QtWidgets import QApplication
    import AssetBrowser.main as main
    import imp
    imp.reload(main)

    for widget in QApplication.topLevelWidgets():
        if widget.objectName() == "PublishTools":
            widget.deleteLater()
    win = main.MainWindow(parent=maya_main_window())
    win.setObjectName('PublishTools')
    win.show()


def createLevel(*args):
    import Tools.maya.createHierarchy as createHierarchy
    createHierarchy.createHierarchy(asset=True)


def createSubGroup(*args):
    import Tools.maya.createHierarchy as createHierarchy
    import Tools.maya.createSubGroup as createSubGroup
    createHierarchy.createHierarchy(asset=True)
    createSubGroup.createSubGroups()

def BatchExport(*args):
    import Tools.maya.BatchExporter as BE
    BE.CreationWindow()


def addJGMenu():

    if cmds.menu('AuroraTools', exists=1):
        cmds.deleteUI('AuroraTools')
    showMyMenu = cmds.menu("AuroraTools", parent="MayaWindow", to=1, aob=1, label=u"AuroraTools")
    cmds.menuItem(parent=showMyMenu, label='Publish', command=open_window)
    cmds.menuItem(parent=showMyMenu, label='CreateHierarchy', command=createLevel)
    cmds.menuItem(parent=showMyMenu, label='CreateSubGroup', command=createSubGroup)
    cmds.menuItem(parent=showMyMenu, label='BatchExport', command=createSubGroup)

cmds.evalDeferred(addJGMenu)