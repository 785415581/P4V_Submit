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

    def initWindow(self, clientRoot):
        self.widget.currentPathCombox.setCurrentText(clientRoot)
        self.rebuildItems(clientRoot)
        self.setTreeWidget(clientRoot)

    def changeType(self, index):
        self.widget.assetNameComboBox.clear()
        currentType = self.widget.typeComboBox.currentText()
        assetPath = os.path.join(self.clientRoot, currentType)
        self.widget.currentPathCombox.setCurrentText(assetPath)
        if os.listdir(assetPath):
            self.widget.assetNameComboBox.addItems(os.listdir(assetPath))

    def changeAsset(self):
        currentType = self.widget.typeComboBox.currentText()
        currentAsset = self.widget.assetNameComboBox.currentText()
        root = "{}/{}/{}".format(self.clientRoot, currentType, currentAsset)
        self.widget.currentPathCombox.clear()
        self.widget.submitStepCom.clear()
        self.widget.currentPathCombox.setCurrentText(root)
        self.setTreeWidget(root, listAll=True)
        self.addSubmitStepCom()

    def addSubmitStepCom(self):
        topItem = self.widget.workTree.topLevelItem(0)
        if topItem.childCount():
            for i in range(topItem.childCount()):
                thisChild = topItem.child(i)
                self.widget.submitStepCom.addItem(thisChild.text(0))
                self.widget.submitStepCom.setItemData(i, thisChild, QtCore.Qt.UserRole)

    def changeTreeStatus(self, index):
        treeWidgetItem = self.widget.submitStepCom.itemData(index, QtCore.Qt.UserRole)
        self.widget.workTree.setCurrentItem(treeWidgetItem)

    def initValue(self):
        value = self.appSetting.getConfig()
        self.widget.serverLn.addItems(value['serverPort'])
        self.widget.workLn.addItems(value['workSpace'])
        self.widget.userLn.addItems(value['user'])

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        actionA = QtWidgets.QAction('New Folder')
        actionB = QtWidgets.QAction('Delete Folder')
        if self.widget.workTree.itemAt(pos):
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
            item.exportType.setEnabled(True)
        else:
            item.exportType.setEnabled(False)

    def addFolder(self, widgets):
        print(widgets)

    def deleteFolder(self, widgets):
        print(widgets)

    def __deleteItem(self, widget):
        items = widget.listWidget.selectedItems()
        for i in range(len(items)):
            itemNum = widget.listWidget.row(items[i])
            item = widget.listWidget.takeItem(itemNum)

    def rebuildItems(self, clientRoot):
        self.widget.typeComboBox.clear()
        self.widget.assetNameComboBox.clear()
        self.widget.typeComboBox.addItems(os.listdir(clientRoot))
        assetRoot = os.path.join(clientRoot, self.widget.typeComboBox.currentText())
        self.widget.assetNameComboBox.addItems(os.listdir(assetRoot))

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
                self.set_tree(child_root, os.path.join(client_asset_name, next_dir_name))
        else:
            root.setText(0, os.path.basename(client_asset_name))
            icon = os.path.dirname(os.path.dirname(__file__)) + '/icons/file.png'
            root.setIcon(0, QtGui.QIcon(icon))

    def publish(self):
        step = self.widget.submitStepCom.currentText()
        if step:
            stepClass = publishInterface.get_step_interface_class(stepName=step)
            print(stepClass)

            # if stepClass:
            #     stepClass().publish()
            # else:
            #     basePublish.BasePublish().publish()

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