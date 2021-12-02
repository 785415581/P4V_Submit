# -*- coding: utf-8 -*-
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
        text, ok = QtWidgets.QInputDialog().getText(QtWidgets.QWidget(), u'修改Label', u'输入文本:')
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
        self.parent = parent
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

        if event.mimeData().hasUrls():
            event.accept()
            for url in event.mimeData().urls():
                localFile = str(url.toLocalFile())
                self.createItem(localFile, source_model="drag", parent_item=currentItem)

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

    def mouseDoubleClickEvent(self, event):

        item = self.itemAt(event.pos())
        # item.setFlags(item.flags() or QtCore.Qt.ItemIsEditable)
        if item:
            inputDialog = QtWidgets.QInputDialog()
            text, ok = inputDialog.getText(self, 'Folder rename', 'input folder name:')
            if ok and text:
                item.setText(0, text)
                item.set_half_path()

    def keyPressEvent(self, event):
        if event.key() == 16777223:
            try:
                currentNodes = self.selectedItems()
                for currNode in currentNodes:
                    currNode = self.currentItem()
                    parent1 = currNode.parent()
                    parent1.removeChild(currNode)
            except Exception:
                try:
                    rootIndex = self.indexOfTopLevelItem(currNode)
                    self.takeTopLevelItem(rootIndex)
                except Exception:
                    print(Exception)


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


# https://blog.csdn.net/LJX4ever/article/details/78039318     reference page
def show_text(function):
    def wrapped(self, *args, **kwargs):
        if self.vars["showTextLock"]:
            self.vars["showTextLock"] = False
            result = function(self, *args, **kwargs)
            items = self.get_selected()
            l = len(items)
            l_ = self.vars["listViewModel"].rowCount() - 1
            self.vars["listViewModel"].item(0).setCheckState(
                QtCore.Qt.Checked if l == l_ else QtCore.Qt.Unchecked if l == 0 else QtCore.Qt.PartiallyChecked)
            self.vars["lineEdit"].setText(
                u"(全选)" if l == l_ else u"(无选择)" if l == 0 else ";".join((item.text() for item in items)))
            self.vars["showTextLock"] = True
        else:
            result = function(self, *args, **kwargs)
        return result

    return wrapped


class QComboCheckBox(QtWidgets.QComboBox):
    class MyListView(QtWidgets.QListView):
        def __init__(self, parent: QtWidgets.QWidget = None, vars=None):
            super().__init__(parent)
            self.vars = vars

        def mousePressEvent(self, event: QtGui.QMouseEvent):
            self.vars["lock"] = False
            super().mousePressEvent(event)

        def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
            self.vars["lock"] = False
            super().mouseDoubleClickEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vars = dict()
        self.vars["lock"] = True
        self.vars["showTextLock"] = True
        # 装饰器锁，避免批量操作时重复改变lineEdit的显示
        self.vars["lineEdit"] = QtWidgets.QLineEdit(self)
        self.vars["lineEdit"].setReadOnly(True)
        self.vars["listView"] = self.MyListView(self, self.vars)
        self.vars["listViewModel"] = QtGui.QStandardItemModel(self)
        self.setModel(self.vars["listViewModel"])
        self.setView(self.vars["listView"])
        self.setLineEdit(self.vars["lineEdit"])

        self.activated.connect(self.__show_selected)

        self.add_item("All select")

    def count(self):
        # 返回子项数
        return super().count() - 1

    @show_text
    def add_item(self, text: "str"):
        # 根据文本添加子项
        item = QtGui.QStandardItem()
        item.setText(text)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Checked)
        self.vars["listViewModel"].appendRow(item)

    @show_text
    def add_items(self, texts: "tuple or list"):
        # 根据文本列表添加子项
        for text in texts:
            self.add_item(text)

    @show_text
    def clear_items(self):
        # 清空所有子项
        self.vars["listViewModel"].clear()
        self.add_item(u"(全选)")

    def find_index(self, index: "int"):
        # 根据索引查找子项
        return self.vars["listViewModel"].item(index if index < 0 else index + 1)

    def find_indexs(self, indexs: "tuple or list"):
        # 根据索引列表查找子项
        return [self.find_index(index) for index in indexs]

    def find_text(self, text: "str"):
        # 根据文本查找子项
        tempList = self.vars["listViewModel"].findItems(text)
        tempList.pop(0) if tempList and tempList[0].row() == 0 else tempList
        return tempList

    def find_texts(self, texts: "tuple or list"):
        # 根据文本列表查找子项
        return {text: self.find_text(text) for text in texts}

    def get_text(self, index: "int"):
        # 根据索引返回文本
        return self.vars["listViewModel"].item(index if index < 0 else index + 1).text()

    def get_texts(self, indexs: "tuple or list"):
        # 根据索引列表返回文本
        return [self.get_text(index) for index in indexs]

    def change_text(self, index: "int", text: "str"):
        # 根据索引改变某一子项的文本
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setText(text)

    @show_text
    def select_index(self, index: "int", state: "bool" = True):
        # 根据索引选中子项，state=False时为取消选中
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setCheckState(
            QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)

    @show_text
    def select_indexs(self, indexs: "tuple or list", state: "bool" = True):
        # 根据索引列表选中子项，state=False时为取消选中
        for index in indexs:
            self.select_index(index, state)

    @show_text
    def select_text(self, text: "str", state: "bool" = True):
        # 根据文本选中子项，state=False时为取消选中
        for item in self.find_text(text):
            item.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)

    @show_text
    def select_texts(self, texts: "tuple or list", state: "bool" = True):
        # 根据文本列表选中子项，state=False时为取消选中
        for text in texts:
            self.select_text(text, state)

    @show_text
    def select_reverse(self):
        # 反转选择
        if self.vars["listViewModel"].item(0).checkState() == QtCore.Qt.Unchecked:
            self.select_all()
        elif self.vars["listViewModel"].item(0).checkState() == QtCore.Qt.Checked:
            self.select_clear()
        else:
            for row in range(1, self.vars["listViewModel"].rowCount()):
                self.__select_reverse(row)

    def __select_reverse(self, row: "int"):
        item = self.vars["listViewModel"].item(row)
        item.setCheckState(QtCore.Qt.Unchecked if item.checkState() == QtCore.Qt.Checked else QtCore.Qt.Checked)

    @show_text
    def select_all(self):
        # 全选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(QtCore.Qt.Checked)

    @show_text
    def select_clear(self):
        # 全不选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(QtCore.Qt.Unchecked)

    @show_text
    def remove_index(self, index: "int"):
        # 根据索引移除子项
        return self.vars["listViewModel"].takeRow(index if index < 0 else index + 1)

    @show_text
    def remove_indexs(self, indexs: "tuple or list"):
        # 根据索引列表移除子项
        return [self.remove_index(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_text(self, text: "str"):
        # 根据文本移除子项
        items = self.find_text(text)
        indexs = [item.row() for item in items]
        return [self.vars["listViewModel"].takeRow(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_texts(self, texts: "tuple or list"):
        # 根据文本列表移除子项
        return {text: self.remove_text(text) for text in texts}

    def get_selected(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.checkState() == QtCore.Qt.Checked:
                items.append(item)
        return items

    def is_all(self):
        # 判断是否是全选
        return True if self.vars["listViewModel"].item(0).checkState() == QtCore.Qt.Checked else False

    def sort(self, order=QtCore.Qt.AscendingOrder):
        # 排序，默认正序
        self.vars["listViewModel"].sort(0, order)

    @show_text
    def __show_selected(self, index):
        if not self.vars["lock"]:
            if index == 0:
                if self.vars["listViewModel"].item(0).checkState() == QtCore.Qt.Checked:
                    self.select_clear()
                else:
                    self.select_all()
            else:
                self.__select_reverse(index)

            self.vars["lock"] = True

    def hidePopup(self):
        if self.vars["lock"]:
            super().hidePopup()


class NoFocusDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        if QStyleOptionViewItem.state & QtWidgets.QStyle.State_HasFocus:
            QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ QtWidgets.QStyle.State_HasFocus
        QtWidgets.QStyledItemDelegate.paint(self, QPainter, QStyleOptionViewItem, QModelIndex)











