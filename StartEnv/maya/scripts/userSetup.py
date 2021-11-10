


def maya_main_window():
    from maya import OpenMayaUI
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def open_window(*args):
    import sys
    sys.path.insert(0, "D:/chenghh/gitlab/publish")

    import AssetBrowser.main as main
    import imp
    imp.reload(main)

    try:
        win.close()
        win.deleteLater()
    except:
        pass

    win = main.MainWindow(parent=maya_main_window())
    win.show()


import maya.cmds as cmds
showMyMenu = cmds.menu(parent="MayaWindow", label=u"JGTools")
cmds.menuItem(parent=showMyMenu, label='Publish', command=open_window)