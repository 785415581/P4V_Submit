# -*- coding: utf-8 -*-
import ctypes
import os
import sys
sys.path.append("R:\ProjectX\Scripts\Python37\Lib\site-packages")
import time
import math
import getpass
from functools import partial

from PySide2 import QtCore, QtWidgets, QtGui
from AssetBrowser.utils.log import ToolsLogger
import AssetBrowser.control.controller as controller
import AssetBrowser.view.main_UI as main_UI
import AssetBrowser.view.baseWidget as baseWidget
import AssetBrowser.modules.app_utils as app_utils

import imp

imp.reload(main_UI)
imp.reload(controller)
imp.reload(baseWidget)

widgets = None


class FloatingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FloatingWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.updateTime = 0
        self.threadExits = 0
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.cycleTimer = QtCore.QTimer()
        self.cycleTimer.timeout.connect(self.updateFloatWindow)
        self.cycleTimer.start(1)
        self.mainWindow = MainWindow(self)
        self.mainWindow.show()
        self.setGeometry(200, 100, 100, 100)
        self.setToolTip("Esc close this window\nDouble click open publish Window")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showHandle)


    def showHandle(self, pos):
        contextMenu = QtWidgets.QMenu()
        contextMenu.setStyleSheet('''
        QMenu {
                background-color: "#242424";
                color: "#D5D5D5";
                border-radius: 2px;
                border: 1px solid #36393f;
                }
    
        QMenu::indicator {
                background-color: "#242424";
                }
        QMenu::item:selected {
                background-color: "#36393f";
                }
        ''')
        contextMenu.setObjectName("contextMenu")
        actionNew = QtWidgets.QAction('Close...')
        contextMenu.addAction(actionNew)
        actionNew.triggered.connect(self.close)
        contextMenu.exec_(QtGui.QCursor().pos())

    def updateFloatWindow(self):
        self.updateTime = (self.updateTime + 0.01) % 314
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            pos = event.pos()
            self.move(event.globalX() - self.piancha.x(), event.globalY() - self.piancha.y())

    def mousePressEvent(self, event):
        self.piancha = event.pos()

    def mouseDoubleClickEvent(self, event):
        if self.mainWindow.isHidden():
            self.mainWindow.move(500, 300)
            self.mainWindow.show()
        else:
            self.mainWindow.setVisible(False)

    def paintEvent(self, event):
        po = QtGui.QPainter(self)
        po.setRenderHint(QtGui.QPainter.Antialiasing)
        po.setBrush(QtGui.QBrush(QtGui.QColor(10, 130, 200)))  # background color
        toppen = QtGui.QPen()
        toppen.setWidth(3)
        toppen.setColor(QtGui.QColor(220, 220, 220))  # Outside the circle
        po.setPen(toppen)
        po.drawEllipse(QtCore.QRect(2, 2, 55, 55))  # Outside the circle size
        # 0a82c8
        po.setPen(QtGui.QColor(255, 255, 200))  # byte dance
        for i in range(10):
            # print(self.updateTime)
            po.drawLine(QtCore.QPoint(i * 5 + 7, 30 + math.sin((i + self.updateTime * 5) / 10) * 10),
                        QtCore.QPoint(i * 5 + 7, 30 + math.sin(((i + 1) + self.updateTime * 7) / 10) * 10))


    def enterEvent(self, event):
        super(FloatingWindow, self).enterEvent(event)
        if self.threadExits == 0:
            self.thear = FloatingWindowEnterThread(self)
            self.threadExits = 1
            self.thear.start()
            self.thear.finished.connect(self.finishSingal)

    def finishSingal(self):
        self.threadExits = 0

    def leaveEvent(self, event):
        super(FloatingWindow, self).leaveEvent(event)
        if self.threadExits == 0:
            self.thear = FloatingWindowLeaveThread(self)
            self.threadExits = 1
            self.thear.start()
            self.thear.finished.connect(self.finishSingal)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.mainWindow.close()
            self.close()


class FloatingWindowLeaveThread(QtCore.QThread):
    def __init__(self, parent):
        super(FloatingWindowLeaveThread, self).__init__()
        self.parent = parent

    def run(self):
        ypos = self.parent.y()
        if ypos < 10:
            for i in range(10):
                self.parent.move(self.parent.x(), ypos - math.sin(3.14159 / 20 * i) * (ypos + 50))
                time.sleep(0.01)
        self.parent.thear.exit()


class FloatingWindowEnterThread(QtCore.QThread):
    finishout = QtCore.Signal(int)

    def __init__(self, parent):
        super(FloatingWindowEnterThread, self).__init__()
        self.parent = parent

    def run(self):
        if self.parent.y() < 0:
            ypos = self.parent.y()
            for i in range(10):
                self.parent.move(self.parent.x(), ypos - math.sin(3.14159 / 20 * i) * (ypos - 5))
                time.sleep(0.01)
        self.parent.thear.exit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args):
        super(MainWindow, self).__init__(parent)
        # super(MainWindow, self).__init__(parent,QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint )
        logger = ToolsLogger.get_logger(getpass.getuser(), save_log=True)
        logger.info("Publish Tools start...")
        self.setWindowTitle(u'Publish for P4V中文')
        self.ui = main_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initStyle()

        global widgets
        widgets = self.ui
        self.control = controller.Controller()

        self.control.view = widgets
        self.control.init()
        self.control.initSignal()
        self.control.appFunction.initUser()

        widgets.currentPathCombox.currentIndexChanged.connect(self.changeCurrentPath)

        widgets.connectBtn.clicked.connect(self.buttonClick)

        widgets.workTree.setDefaultDropAction(QtCore.Qt.CopyAction)
        widgets.workTree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        widgets.assets_file_list.setAcceptDrops(True)
        widgets.assets_file_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        widgets.assets_file_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        widgets.assets_file_list.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        widgets.passwordLn.installEventFilter(self)
        # widgets.assetNameComboBox.installEventFilter(self)


    def initStyle(self):
        stylePath = "{}/{}".format(os.path.dirname(__file__), 'resources/style.qss')
        fp = open(stylePath, 'r')
        style = fp.read()
        self.setStyleSheet(style)

        window_pale = QtGui.QPalette()
        window_pale.setColor(QtGui.QPalette.Background, QtGui.QColor(54, 57, 63))
        self.setPalette(window_pale)


    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.DragEnter:
            if watched is self.ui.assets_file_list:
                event.accept()
                return True
        elif event.type() == QtCore.QEvent.Drop:
            if watched is self.ui.assets_file_list:
                data = event.mimeData()
                urls = data.urls()
                for url in urls:
                    filePath = url.toLocalFile()
                    item = baseWidget.ListWidgetItem(self.ui.assets_file_list)
                    item.filePath = filePath
                    item.setCurrentEnterFile(os.path.basename(filePath))
                    widgets.listWidget.addItem(item)
                    item.exportCheck.clicked.connect(partial(self.control.appFunction.checkedExportItem, item))
                    item.exportPath.clicked.connect(partial(self.control.appFunction.selectExportPath, item))

        elif event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if watched is self.ui.passwordLn:
                if key == 16777220:
                    self.buttonClick()

        return QtCore.QObject.eventFilter(self, watched, event)

    def changeCurrentPath(self, index):
        pass
        # treeWidgetItem = widgets.currentPathCombox.itemData(index, QtCore.Qt.UserRole)
        # widgets.workTree.setCurrentItem(treeWidgetItem)

    def buttonClick(self):

        app_utils.add_log("Start Connect perforce...")
        self.control.p4Model.user = self.ui.userLn.currentText()
        self.control.p4Model.password = self.ui.passwordLn.text()
        self.control.p4Model.validation()
        self.control.p4Model.initAssetsClient()
        clientRoot = self.control.p4Model.getRoot()
        app_utils.add_log("Finish Connect perforce...")
        app_utils.add_log("clientRoot = {}".format(clientRoot))
        clientStream = self.control.p4Model.getStreamName()
        app_utils.add_log("clientStream = {}".format(clientStream))
        if clientStream:
            self.control.appFunction.validation = self.control.p4Model.validation
            self.control.appFunction.clientRoot = clientRoot
            self.control.appFunction.clientStream = clientStream
            self.control.appFunction.initWindow()
        else:
            app_utils.add_log("Failed to get stream:{0}".format(clientStream), error=True)

    def closeEvent(self, event):
        event.accept()
        self.control.appFunction.callBack()


if __name__ == '__main__':

    # app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
    # window = MainWindow()
    # window.show()
    # app.exec_()
    app = QtWidgets.QApplication(sys.argv)
    for o in QtWidgets.QApplication.topLevelWidgets():
        if o.objectName() == "FloatingWindow":
            o.deleteLater()
    FloatingBall = FloatingWindow()
    FloatingBall.show()
    app.exec_()