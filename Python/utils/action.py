from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class ActionGeneral:
    contextMenuTree = QtWidgets.QMenu()

    def newFolderSolider(self):
        actionA = QtWidgets.QAction('New Folder')