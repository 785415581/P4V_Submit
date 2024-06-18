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

def ExportLOD(*args):
    import Tools.maya.CreateLODGroup.createLODGroup as CLODG
    from PySide2.QtWidgets import QApplication
    import imp
    imp.reload(CLODG)

    for widget in QApplication.topLevelWidgets():
        if widget.objectName() == "ExportLODManage":
            widget.deleteLater()
    win = CLODG.ExportLOD(parent=maya_main_window())
    win.setObjectName('ExportLODManage')
    win.show()

def CallPyblish(*args):
    from Tools.maya.Pyblish.pyblish import api
    api.register_gui("pyblish_qml")
    api.register_plugin_path(r"D:\workSpace\Maya\Pyblish\pyblish_plugins\model")

    # 2. Set-up Pyblish for Maya
    import Tools.maya.Pyblish.pyblish_maya as pyblish_maya
    pyblish_maya.setup()

    import Tools.maya.Pyblish.pyblish_qml as pyblish_qml
    pyblish_qml.show()

def addJGMenu():

    if cmds.menu('AuroraTools', exists=1):
        cmds.deleteUI('AuroraTools')
    showMyMenu = cmds.menu("AuroraTools", parent="MayaWindow", to=1, aob=1, label=u"AuroraTools")
    cmds.menuItem(parent=showMyMenu, label='Publish', command=open_window)
    cmds.menuItem(parent=showMyMenu, label='CreateHierarchy', command=createLevel)
    cmds.menuItem(parent=showMyMenu, label='CreateSubGroup', command=createSubGroup)
    cmds.menuItem(parent=showMyMenu, label='BatchExport', command=BatchExport)
    cmds.menuItem(parent=showMyMenu, label='Export LOD', command=ExportLOD)
    cmds.menuItem(parent=showMyMenu, label='Pyblish', command=CallPyblish)


cmds.evalDeferred(addJGMenu)