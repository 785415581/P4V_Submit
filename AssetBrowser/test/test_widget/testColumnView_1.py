#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/2 12:00
"""

import sys
import os
import abc
import json
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


class TreeItemModel(QtCore.QAbstractItemModel):

    def __init__(self, root, parent=None):
        super(TreeItemModel, self).__init__(parent)
        self._root_item = root
        self._header = self._root_item.header()

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return len(self._header)

    def data(self, index, role):
        if index.isValid():
            # return QVariant()
            item = index.internalPointer()

            if role == QtCore.Qt.DisplayRole:
                return item.data(index.column())
            elif role == QtCore.Qt.ItemDataRole:
                return item.data(index.column())
            # else:
            #     print('not recognised')

        # if role == Qt.DisplayRole:
        #     return item.data(index.column())
        # if role == Qt.UserRole:
        #     if item:
        #         return item.person
        # return QVariant()

    def headerData(self, column, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            try:
                return self._header[column]
            except IndexError:
                pass
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child_at(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        if not child_item:
            return QtCore.QModelIndex()
        parent_item = child_item.parent()
        if parent_item == self._root_item:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()


class AbstractTreeItem(object, metaclass=abc.ABCMeta):

    def __init__(self, parent=None):
        self._children = None
        self._parent = parent

    @abc.abstractmethod
    def header(self):
        raise NotImplementedError(self.header)

    @abc.abstractmethod
    def column_count(self):
        raise NotImplementedError(self.column_count)

    def parent(self):
        return self._parent

    @abc.abstractmethod
    def _create_children(self):
        return []

    def row(self):
        if self._parent:
            return self._parent._children.index(self)
        return 0

    @property
    def children(self):
        if self._children is None:
            self._children = self._create_children()
        return self._children

    def child_at(self, row):
        return self.children[row]

    @abc.abstractmethod
    def data(self, column):
        raise NotImplementedError(self.data)

    def child_count(self):
        count = len(self.children)
        return count


class DirPathModel(AbstractTreeItem):

    def __init__(self, root, parent=None):
        super(DirPathModel, self).__init__(parent)
        self._root = root

    def _create_children(self):
        children = []
        try:
            entries = self._root.keys()
        except OSError:
            entries = []
        for name in entries:
            fn = self._root.get(name)
            if fn:
                children.append(self.__class__(fn, self))
        return children

    def data(self, column):
        # return os.path.basename(self._root)
        # return self._root
        return '222'

    def header(self):
        return ["name"]

    def column_count(self):
        return 1


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QColumnView()
    view.setWindowTitle("Dynamic Column view test")
    view.resize(1024, 768)

    view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    view.customContextMenuRequested.connect(lambda: showContextMenu(view))


    with open('FileStructure.json') as fp:
        data = json.load(fp)
    root = DirPathModel(data)
    model = TreeItemModel(root)
    view.setModel(model)
    view.show()
    return app.exec_()


def showContextMenu(view):
    view.contextMenu = QtWidgets.QMenu()
    actionA = view.contextMenu.addAction(u'动作a')

    view.contextMenu.popup(QtGui.QCursor.pos())  # 2菜单显示的位置
    actionA.triggered.connect(lambda: actionHandler(view))

    view.contextMenu.show()


def actionHandler(view):
    print(view)
    print(view.currentIndex())
    print(view.currentIndex().data())
    print(view.currentIndex().row())
    print(view.currentIndex().parent().row())
    print("成功")


if __name__ == "__main__":
    sys.exit(main() or 0)
