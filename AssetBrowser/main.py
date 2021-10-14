# -*- coding: utf-8 -*-
import ctypes
import os
import sys
sys.path.append("R:\ProjectX\Scripts\Python37\Lib\site-packages")
from functools import partial

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import AssetBrowser.publishInterface as publishInterface
import AssetBrowser.control.controller as controller
import AssetBrowser.modules.ui_main as ui_main
import AssetBrowser.view.baseWidget as baseWidget

import imp
imp.reload(publishInterface)
imp.reload(controller)
imp.reload(ui_main)
imp.reload(baseWidget)


widgets = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args):
        super(MainWindow, self).__init__(parent)

        #todo treewidget waiting to deal with fold and file item
        #todo darg fold need to do
        #todo mark full path or half path on item,need to solve fold and file
        self.setWindowTitle(u'Publish for P4V中文')
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.control = controller.Controller()
        self.control.view = widgets
        self.control.init()
        self.control.initSignal()
        self.control.appFunction.initUser()

        widgets.currentPathCombox.currentIndexChanged.connect(self.changeCurrentPath)

        widgets.connectBtn.clicked.connect(self.buttonClick)
        widgets.publishBtn.clicked.connect(self.buttonClick)


        widgets.workTree.setDefaultDropAction(QtCore.Qt.CopyAction)
        widgets.workTree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        widgets.assets_file_list.setAcceptDrops(True)
        widgets.assets_file_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        widgets.assets_file_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        widgets.assets_file_list.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        widgets.assets_file_list.installEventFilter(self)
        widgets.assetNameComboBox.installEventFilter(self)

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
            if watched is self.ui.assetNameComboBox:
                key = event.key()
                if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
                    pass
                    # self.control.createAsset(self.control)
            elif watched is self.ui.submitStepCom:
                print('222')
        return QtCore.QObject.eventFilter(self, watched, event)

    def changeCurrentPath(self, index):
        treeWidgetItem = widgets.currentPathCombox.itemData(index, QtCore.Qt.UserRole)
        widgets.workTree.setCurrentItem(treeWidgetItem)



    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "connectBtn":
            self.control.p4Model.user = self.ui.userLn.currentText()
            self.control.p4Model.password = self.ui.passwordLn.text()

            self.control.p4Model.validation()
            self.control.p4Model.initAssetsClient()
            clientRoot = self.control.p4Model.getRoot()
            print("clientRoot = {}".format(clientRoot))
            clientStream = self.control.p4Model.getStreamName()
            print("clientStream = {}".format(clientStream))
            if clientStream:
                self.control.appFunction.validation = self.control.p4Model.validation
                self.control.appFunction.clientRoot = clientRoot
                self.control.appFunction.clientStream = clientStream
                self.control.appFunction.initWindow()
            else:
                print('error')
        elif btnName == "publishBtn":
            step = self.control.appFunction.submitStepComText
            if step:
                stepClass = publishInterface.get_step_interface_class(stepName=step)
                Interface = stepClass()
                Interface.control = self.control
                Interface.publish()
            print('publishBtn')
        elif btnName == "exportBtn":

            pass


    def closeEvent(self, event):
        event.accept()
        self.control.appFunction.callBack()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Hero_Publish')
    window = MainWindow()
    window.show()
    app.exec_()
