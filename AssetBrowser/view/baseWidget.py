# _*_coding:utf-8 _*_
import os
import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class ListWidgetItem(QtWidgets.QListWidgetItem):
    itemChecked = QtCore.Signal(str)

    def __init__(self, parent):
        super(ListWidgetItem, self).__init__(parent)
        self._filePath = None
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.fileBaseName = QtWidgets.QLabel()
        self.fileBaseName.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.exportCheck = QtWidgets.QCheckBox('Export')
        self.exportType = QtWidgets.QComboBox()
        self.exportType.addItems(['fbx', 'mesh'])
        self.exportType.setEnabled(False)
        self.exportPath = QtWidgets.QPushButton('...')
        self.exportPath.setEnabled(False)
        self.exportPath.exportDirectory = None
        self.item_layout = QtWidgets.QHBoxLayout()
        self.item_layout.addWidget(self.fileBaseName)
        self.item_layout.addWidget(self.exportCheck)
        self.item_layout.addWidget(self.exportType)
        self.item_layout.addWidget(self.exportPath)
        self.item_layout.setStretch(0, 5)
        self.item_layout.setContentsMargins(0, 0, 0, 0)

        self.widget.setLayout(self.item_layout)
        self.setSizeHint(self.widget.sizeHint())
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)

    def setCurrentEnterFile(self, fileName):
        self.fileBaseName.setText(fileName)

    def mouseDoubleClickEvent(self, event):
        text, ok = QtWidgets.QInputDialog().getText(QtWidgets.QWidget(), '修改Label', '输入文本:')
        if ok and text:
            self.fileBaseName.setText(text)

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        self._filePath = value
