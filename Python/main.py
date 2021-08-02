import os
import sys
import ctypes
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import qdarkstyle
from Python.modules.ui_main import Ui_MainWindow
from Python.control.controller import Controller
from Python.view.baseWidget import ListWidgetItem
from Python import publishInterface
from Python.utils import utils
widgets = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Publish for P4V')
        self.currentPathList = list()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.control = Controller(widgets)
        self.control.initSignal()
        self.control.appFunction.initValue()
        widgets.currentPathCombox.currentIndexChanged.connect(self.changeCurrentPath)
        widgets.workTree.itemClicked.connect(self.listPath)
        widgets.connectBtn.clicked.connect(self.buttonClick)
        widgets.publishBtn.clicked.connect(self.buttonClick)
        widgets.listWidget.setAcceptDrops(True)
        widgets.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        widgets.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        widgets.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        widgets.listWidget.installEventFilter(self)
        widgets.assetNameComboBox.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.DragEnter:
            if watched is self.ui.listWidget:
                event.accept()
                return True
        elif event.type() == QtCore.QEvent.Drop:
            if watched is self.ui.listWidget:
                data = event.mimeData()
                urls = data.urls()
                for url in urls:
                    filePath = url.toLocalFile()
                    item = ListWidgetItem(self.ui.listWidget)
                    item.filePath = filePath
                    item.setCurrentEnterFile(os.path.basename(filePath))
                    widgets.listWidget.addItem(item)
                    item.exportCheck.clicked.connect(partial(self.control.appFunction.checkedExportItem, item))
        elif event.type() == QtCore.QEvent.KeyPress:
            if watched is self.ui.assetNameComboBox:
                key = event.key()
                if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
                    self.control.createAsset(self.control)
            elif watched is self.ui.submitStepCom:
                print('222')
        return QtCore.QObject.eventFilter(self, watched, event)

    def changeCurrentPath(self, index):
        treeWidgetItem = widgets.currentPathCombox.itemData(index, QtCore.Qt.UserRole)
        widgets.workTree.setCurrentItem(treeWidgetItem)

    def listPath(self, item, column):
        res = self.getCurrentPath(item)
        print(res)
        if self.control.appFunction.clientRoot and res not in self.currentPathList:
            widgets.currentPathCombox.addItem(res.replace('\\', '/'))
            self.currentPathList.append(res)
            index = widgets.currentPathCombox.count()
            widgets.currentPathCombox.setItemData(index-1, item, QtCore.Qt.UserRole)
        widgets.currentPathCombox.setCurrentText(res.replace('\\', '/'))

    def getCurrentPath(self, item, strPath=''):
        if item.parent():
            parentWidget = item.parent()
            currentFolderName = item.text(0)
            if strPath:
                strPath = currentFolderName + '/' + strPath
            else:
                strPath = currentFolderName
            return self.getCurrentPath(parentWidget, strPath)
        else:
            currentType = widgets.typeComboBox.currentText()
            currentAsset = widgets.assetNameComboBox.currentText()
            currentPath = os.path.join(self.control.appFunction.clientRoot, currentType, currentAsset, strPath)
            return currentPath

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "connectBtn":
            self.control.init()
            self.control.initUI()
            p4Info = self.control.p4Model.connectP4()
            if p4Info and p4Info[0].get('clientRoot', ''):
                clientRoot = p4Info[0]['clientRoot']
                self.control.appFunction.clientRoot = clientRoot
                self.control.appFunction.initWindow(clientRoot)

        elif btnName == "publishBtn":
            step = self.control.appFunction.submitStepComText
            if step:
                stepClass = publishInterface.get_step_interface_class(stepName=step)
                Interface = stepClass()
                Interface.appFunction = self.control.appFunction
                Interface.p4Model = self.control.p4Model
                Interface.view = self.control.view
                Interface.publish()
            print('publishBtn')

    def closeEvent(self, event):
        event.accept()
        self.control.appFunction.callBack()
        self.control.p4Model.disconnectP4()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Hero_Publish')
    window = MainWindow()
    window.show()
    app.exec_()