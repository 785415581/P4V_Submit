import os
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from Python.modules.app_setting import AppSetting
from Python import publishInterface
from Python.publish_hooks import basePublish


class AppFunction(object):

    def __init__(self, ui):
        self.appSetting = AppSetting()
        self.widget = ui
        self._clientRoot = None

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, clientRoot):
        self._clientRoot = clientRoot

    @property
    def typeComboBoxText(self):
        return self.widget.typeComboBox.currentText()

    @property
    def assetNameComboBoxText(self):
        return self.widget.assetNameComboBox.currentText()

    @property
    def submitStepComText(self):
        return self.widget.submitStepCom.currentText()

    def initWindow(self, clientRoot):
        self.widget.typeComboBox.blockSignals(True)
        self.widget.assetNameComboBox.blockSignals(True)
        self.widget.currentPathCombox.setCurrentText(clientRoot)
        self.widget.typeComboBox.clear()
        self.widget.assetNameComboBox.clear()
        self.widget.submitStepCom.clear()
        for i in os.listdir(clientRoot):
            self.widget.typeComboBox.addItem(i, os.path.join(clientRoot, i))
        indexType = self.widget.typeComboBox.currentIndex()
        currentType = self.widget.typeComboBox.itemData(indexType, role=QtCore.Qt.UserRole)
        self.setTreeWidget(currentType)
        self.widget.typeComboBox.blockSignals(False)
        self.widget.assetNameComboBox.blockSignals(False)

    def changeType(self, index):
        self.widget.assetNameComboBox.clear()
        currentType = self.widget.typeComboBox.itemData(index, role=QtCore.Qt.UserRole)
        self.widget.currentPathCombox.setCurrentText(currentType)
        self.widget.assetNameComboBox.addItem('')
        if os.listdir(currentType):
            for i in os.listdir(currentType):
                self.widget.assetNameComboBox.addItem(i, os.path.join(currentType, i))
        self.setTreeWidget(currentType, listAll=True)

    def changeAsset(self, index):
        currentAsset = self.widget.assetNameComboBox.itemData(index, role=QtCore.Qt.UserRole)
        if currentAsset:
            self.widget.currentPathCombox.setCurrentText(currentAsset)
            self.widget.currentPathCombox.clear()
            self.widget.submitStepCom.clear()
            self.widget.submitStepCom.addItem('', None)
            for i in os.listdir(currentAsset):
                self.widget.submitStepCom.addItem(i, os.path.join(currentAsset, i))
            self.setTreeWidget(currentAsset, listAll=True)
        else:
            indexType = self.widget.typeComboBox.currentIndex()
            currentType = self.widget.typeComboBox.itemData(indexType, role=QtCore.Qt.UserRole)
            self.widget.currentPathCombox.setCurrentText(currentType)
            self.widget.submitStepCom.clear()
            self.setTreeWidget(currentType, listAll=True)

    def changeStep(self, index):
        currentStep = self.widget.submitStepCom.itemData(index, role=QtCore.Qt.UserRole)
        if currentStep:
            self.widget.currentPathCombox.clear()
            self.widget.currentPathCombox.setCurrentText(currentStep)
            self.setTreeWidget(currentStep, listAll=True)

    def initValue(self):
        value = self.appSetting.getConfig()
        self.widget.serverLn.addItems(value['serverPort'])
        self.widget.workLn.addItems(value['workSpace'])
        self.widget.userLn.addItems(value['user'])

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        actionA = QtWidgets.QAction('New Folder')
        actionB = QtWidgets.QAction('Delete Folder')
        actionC = QtWidgets.QAction('Import Unreal')
        if self.widget.workTree.itemAt(pos):
            item = self.widget.workTree.itemAt(pos)
            currentTreeItemPath = item.whatsThis(0)
            if os.path.isfile(currentTreeItemPath):
                contextMenuTree.addAction(actionC)
                actionC.triggered.connect(lambda: self.importAsset(self.widget))
            contextMenuTree.addAction(actionA)
            contextMenuTree.addAction(actionB)
            actionA.triggered.connect(lambda: self.addFolder(self.widget))
            actionB.triggered.connect(lambda: self.deleteFolder(self.widget))
        contextMenuTree.exec_(QtGui.QCursor().pos())

    def showWorkListHandle(self, pos):
        contextMenuList = QtWidgets.QMenu()
        delAct = QtWidgets.QAction('Delete Item')
        if self.widget.listWidget.itemAt(pos):
            contextMenuList.addAction(delAct)
            delAct.triggered.connect(lambda: self.__deleteItem(self.widget))
        contextMenuList.exec_(QtGui.QCursor().pos())

    def checkedExportItem(self, item):
        if item.exportCheck.isChecked():
            print(item.fileBaseName.text())
            print(item.filePath)
            item.exportType.setEnabled(True)
        else:
            item.exportType.setEnabled(False)

    def addFolder(self, widgets):
        print(widgets)

    def deleteFolder(self, widgets):
        print(widgets)

    def importAsset(self, widgets):
        print(widgets)

    def __deleteItem(self, widget):
        items = widget.listWidget.selectedItems()
        for i in range(len(items)):
            itemNum = widget.listWidget.row(items[i])
            item = widget.listWidget.takeItem(itemNum)

    def setTreeWidget(self, clientRoot, listAll=False):
        self.widget.workTree.clear()
        root = QtWidgets.QTreeWidgetItem(self.widget.workTree)
        root.setExpanded(True)
        root.setText(0, os.path.basename(clientRoot))
        if listAll:
            self.set_tree(root, clientRoot)
        else:
            next_dir = os.listdir(clientRoot)
            for next_dir_name in next_dir:
                currentPath = os.path.join(clientRoot, next_dir_name)
                child_root = QtWidgets.QTreeWidgetItem(root)
                child_root.setText(0, os.path.basename(next_dir_name))
                if os.path.isdir(currentPath):
                    icon = os.path.dirname(os.path.dirname(__file__)) + '/icons/close_folder.png'
                    child_root.setIcon(0, QtGui.QIcon(icon))

    def set_tree(self, root, client_asset_name):
        if os.path.isdir(client_asset_name):
            next_dir = os.listdir(client_asset_name)
            for next_dir_name in next_dir:
                child_root = QtWidgets.QTreeWidgetItem(root)
                child_root.setText(0, os.path.basename(next_dir_name))
                child_root.setWhatsThis(0, os.path.join(client_asset_name, next_dir_name))
                self.set_tree(child_root, os.path.join(client_asset_name, next_dir_name))
        else:
            root.setText(0, os.path.basename(client_asset_name))
            icon = os.path.dirname(os.path.dirname(__file__)) + '/icons/file.png'
            root.setIcon(0, QtGui.QIcon(icon))


    def callBack(self):
        self.appSetting.init()
        configValue = self.appSetting.getConfig()
        serverPort = self.widget.serverLn.currentText()
        user = self.widget.userLn.currentText()
        workSpace = self.widget.workLn.currentText()
        if serverPort not in configValue['serverPort']:
            configValue['serverPort'].append(serverPort)
        if user not in configValue['user']:
            configValue['user'].append(user)
        if workSpace not in configValue['workSpace']:
            configValue['workSpace'].append(workSpace)
        self.appSetting.setConfig(configValue)