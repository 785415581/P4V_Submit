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
        self.widget = QtWidgets.QWidget(parent)
        self.fileBaseName = QtWidgets.QLabel()
        self.exportCheck = QtWidgets.QCheckBox('Export')
        self.exportType = QtWidgets.QComboBox()
        self.exportType.addItems(['fbx', 'mesh'])
        self.exportType.setEnabled(False)
        self.item_layout = QtWidgets.QHBoxLayout()
        self.item_layout.addWidget(self.fileBaseName)
        self.item_layout.addWidget(self.exportCheck)
        self.item_layout.addWidget(self.exportType)
        self.item_layout.setStretch(0, 5)
        self.item_layout.setContentsMargins(0, 0, 0, 0)
        self.item_layout.addStretch(1)
        self.widget.setLayout(self.item_layout)
        self.setSizeHint(self.widget.sizeHint())
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)

    def setCurrentEnterFile(self, fileName):
        self.fileBaseName.setText(fileName)

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        self._filePath = value