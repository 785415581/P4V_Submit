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


class PathTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, source_path, source_model="local", parent=None):
        super(PathTreeItem, self).__init__(parent)
        self.setText(0, source_path.replace("\\", "/").split("/")[-1])

        self.parentItem = None
        self.half_path = ""
        self.source_path = source_path
        self.source_model = source_model
        self.childItems = []
        self.have_rev = None

        #todo waiting to debug type

        flag = isinstance(parent, QtWidgets.QTreeWidgetItem)
        if flag:
            self.parentItem = parent
            self.parentItem.childItems.append(self)

        self.set_half_path()

    def set_half_path(self):
        current_text = "/"+self.text(0)
        if self.parentItem:
            self.half_path = self.parentItem.half_path + current_text
        else:
            self.half_path = current_text

        """
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setWhatsThis(0, leafName['path'])
        item.setText(0, os.path.basename(leafName['name']))
        """





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



    def createItem(self, real_path, parent_item=None, source_model=None):
        real_path = real_path.replace("\\", "/")
        if parent_item:
            current_item = PathTreeItem(real_path, source_model=source_model, parent=parent_item)
        else:
            current_item = PathTreeItem(real_path, source_model=source_model, parent=self)

        if os.path.isdir(real_path):
            for root, dirs, files in os.walk(real_path):

                parent_item = current_item
                for dir in dirs:
                    dir_full_path = os.path.join(root, dir)
                    self.createItem(dir_full_path, source_model=source_model, parent_item=parent_item)

                for file in files:
                    file_full = os.path.join(root, file)
                    PathTreeItem(file_full, source_model=source_model, parent=parent_item)
                return

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.accept()


    def dropEvent(self, event):

        currentItem = self.itemAt(event.pos())
        if currentItem and ("." in currentItem.text(0)) and (not currentItem.childItems):
            return

        drag_file = event.mimeData().text()
        if event.mimeData().hasFormat("text/uri-list"):
            real_path = drag_file.split("file:///")[-1]
            self.createItem(real_path, source_model="drag", parent_item=currentItem)
        #todo waiting to replace with copy drag item
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            source_widget = event.source()
            items = source_widget.selectedItems()
            for item in items:
                parentItem = currentItem if currentItem else self
                self.accept_drag_items(item, parentItem)


    def accept_drag_items(self, customItem, parentItem):
        new_item = PathTreeItem(customItem.source_path, source_model="server", parent=parentItem)
        for child_item in customItem.childItems:
            self.accept_drag_items(child_item, new_item)


    def dragMoveEvent(self, event):
        if event.source:
            if event.mimeData().hasFormat("text/uri-list"):
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                event.accept()

            else:
                event.ignore()


class CustomModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[], headers = []):
        super(CustomModel, self).__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def data(self, index, role=QtGui.Qt.DisplayRole):
        if index.isValid():
            if role == QtGui.Qt.DisplayRole or role == QtGui.Qt.EditRole:
                value = self._data[index.row()][index.column()]
                return value

    def setData(self, data):
        self.beginResetModel()
        self._data =data
        self.endResetModel()
        return True

    def flags(self, index):
        return QtGui.Qt.ItemIsSelectable | QtGui.Qt.ItemIsEnabled | QtGui.Qt.ItemIsEditable


    def headerData(self, int, orientation, role):
        if orientation != QtCore.Qt.Horizontal:
            return
        if role == QtCore.Qt.DisplayRole:
            return self._headers[int]

    def set_header_data(self, heads):
        self._headers = heads
        for headix, head in enumerate(self._headers):
            self.setHeaderData(headix, QtCore.Qt.Horizontal, head, role=QtCore.Qt.DisplayRole)



class LogPlainText(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super(LogPlainText, self).__init__(parent)

















