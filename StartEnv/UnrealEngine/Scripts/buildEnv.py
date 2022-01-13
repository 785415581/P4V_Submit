#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/10 17:58
"""
import os
import sys
import imp
import ctypes
import unreal
from PySide2 import QtGui
from PySide2 import QtWidgets

from AssetBrowser import main
imp.reload(main)
from Tools.unreal_tools import main_tools


def mainFunc():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon(r"R:\ProjectX\Scripts\Python\tools\publish\AssetBrowser/resources/icons/icon.ico"))
    global window

    window = main.MainWindow()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Hero_Publish')
    window.show()
    unreal.parent_external_window_to_slate(window.winId())


def Tools():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon(r"R:\ProjectX\Scripts\Python\tools\publish\AssetBrowser/resources/icons/icon.ico"))
    global window

    window = main_tools.View()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Hero_Publish')
    window.show()
    unreal.parent_external_window_to_slate(window.winId())