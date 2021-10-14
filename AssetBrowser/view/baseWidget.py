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



class TreeWidgetDrop(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(TreeWidgetDrop, self).__init__(parent)

        self.setHeaderHidden(True)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.formerIndex = None



    def createItem(self, real_path, parent_item=None):
        file_name = real_path.replace("\\", "/")
        file_name = file_name.split("/")[-1]

        if parent_item:
            current_item = QtWidgets.QTreeWidgetItem(parent_item)
            current_item.setText(0, file_name)
        else:
            current_item = QtWidgets.QTreeWidgetItem(self)
            current_item.setText(0, file_name)

        if os.path.isfile(real_path):
            current_item.setWhatsThis(0, "fullPath:"+ real_path)

        parent_item_dict = {}
        parent_item_dict[real_path] = current_item
        if os.path.isdir(real_path):
            for root, dirs, files in os.walk(real_path):
                parent_item = parent_item_dict[root]
                for dir in dirs:
                    item = QtWidgets.QTreeWidgetItem(parent_item)
                    item.setText(0, dir)

                    dir_full_path = os.path.join(root, dir)
                    parent_item_dict[dir_full_path] = item
                for file in files:
                    item = QtWidgets.QTreeWidgetItem(parent_item)
                    item.setWhatsThis(0, "fullPath:"+os.path.join(root, file))
                    item.setText(0, file)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.accept()


    def dropEvent(self, event):

        #todo copy file, then judge add or checkout
        currentItem = self.itemAt(event.pos())
        drag_file = event.mimeData().text()
        if event.mimeData().hasFormat("text/uri-list"):
            real_path = drag_file.split("file:///")[-1]

            self.createItem(real_path, currentItem)
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            source_widget = event.source()
            items = source_widget.selectedItems()
            for item in items:
                if currentItem:
                    insert_item = QtWidgets.QTreeWidgetItem(currentItem)
                else:
                    insert_item = QtWidgets.QTreeWidgetItem(self)
                insert_item.setText(0, item.text(0))
                insert_item.setWhatsThis(0, item.whatsThis(0))



    def dragMoveEvent(self, event):
        if event.source:
            if event.mimeData().hasFormat("text/uri-list"):
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                event.accept()

            else:
                event.ignore()

