#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/2 11:50
"""
import json
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDir
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QMainWindow, QColumnView, QFileSystemModel


class DemoColumnView(QMainWindow):
    def __init__(self, parent=None):
        super(DemoColumnView, self).__init__(parent)
        self.setWindowTitle('实战PyQt5: QColumnView 演示')
        self.resize(480, 300)
        self.initUi()

    def initUi(self):
        columnView = QColumnView(self)
        model = QStandardItemModel()
        with open('FileStructure.json') as fp:
            data = json.load(fp)
        self.setData(data, parentItem=model)
        columnView.setModel(model)
        self.setCentralWidget(columnView)

    def setData(self, data, parentItem=None):
        for group, value in data.items():
            subItem = QStandardItem(group)
            parentItem.appendRow(subItem)
            self.setData(value, parentItem=subItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoColumnView()
    window.show()
    app.exec_()
