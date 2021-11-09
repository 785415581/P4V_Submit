#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/10/13 16:06
"""

from PySide2 import QtWidgets
from PySide2 import QtUiTools
from PySide2 import QtCore
import MyWidget


class MainWindow(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.ui = QtUiTools.QUiLoader().load('./mainwindow.ui')

        self.ui.file_path.deleteLater()  # 删除原有的路径框
        self.ui.file_path = MyWidget.MyQLine()  # 新建自己的替换原有的
        self.ui.file_path.setPlaceholderText('浏览或拖拽SRT字幕文件到这里')
        self.ui.horizontalLayout_2.addWidget(self.ui.file_path)
        self.ui.horizontalLayout_2.addWidget(self.ui.file)

