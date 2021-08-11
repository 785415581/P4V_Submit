import os
import subprocess
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from Python.modules.app_setting import AppSetting
from Python.utils.Leaf import Leaf
from Python.utils.utils import Utils
from Python import publishInterface
from Python.publish_hooks import basePublish


class AppFunction(object):

    def __init__(self):
        self.appSetting = AppSetting()
        self._view = None
        self._clientRoot = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, clientRoot):
        self._clientRoot = clientRoot

    @property
    def typeComboBoxText(self):
        return self.view.typeComboBox.currentText()

    @property
    def assetNameComboBoxText(self):
        return self.view.assetNameComboBox.currentText()

    @property
    def submitStepComText(self):
        return self.view.submitStepCom.currentText()

    def initWindow(self):
        self.view.typeComboBox.blockSignals(True)
        self.view.assetNameComboBox.blockSignals(True)
        self.view.currentPathCombox.setCurrentText(self.clientRoot)
        self.view.typeComboBox.clear()
        self.view.assetNameComboBox.clear()
        self.view.submitStepCom.clear()
        for i in Utils.listdir(self.clientRoot):
            self.view.typeComboBox.addItem(i, "{}/{}".format(self.clientRoot, i))

        indexType = self.view.typeComboBox.currentIndex()
        currentType = self.view.typeComboBox.itemData(indexType, role=QtCore.Qt.UserRole)
        self.setTreeWidget(currentType)
        self.view.typeComboBox.blockSignals(False)
        self.view.assetNameComboBox.blockSignals(False)

    def changeType(self, index):
        self.view.assetNameComboBox.clear()
        currentType = self.view.typeComboBox.itemData(index, role=QtCore.Qt.UserRole)
        self.view.currentPathCombox.setCurrentText(currentType)
        self.view.assetNameComboBox.addItem('')
        for i in Utils.listdir(currentType):
            self.view.assetNameComboBox.addItem(i, "{}/{}".format(currentType, i))
        self.setTreeWidget(currentType)

    def changeAsset(self, index):
        currentAsset = self.view.assetNameComboBox.itemData(index, role=QtCore.Qt.UserRole)
        if currentAsset:
            self.view.currentPathCombox.setCurrentText(currentAsset)
            self.view.currentPathCombox.clear()
            self.view.submitStepCom.clear()
            self.view.submitStepCom.addItem('', None)
            for i in Utils.listdir(currentAsset):
                self.view.submitStepCom.addItem(i, "{}/{}".format(currentAsset, i))
            self.setTreeWidget(currentAsset)
        else:
            indexType = self.view.typeComboBox.currentIndex()
            currentType = self.view.typeComboBox.itemData(indexType, role=QtCore.Qt.UserRole)
            self.view.currentPathCombox.setCurrentText(currentType)
            self.view.submitStepCom.clear()
            self.setTreeWidget(currentType)

    def changeStep(self, index):
        currentStep = self.view.submitStepCom.itemData(index, role=QtCore.Qt.UserRole)
        if currentStep:
            self.view.currentPathCombox.clear()
            self.view.currentPathCombox.setCurrentText(currentStep)
            self.setTreeWidget(currentStep)

    def initValue(self):
        value = self.appSetting.getConfig()
        self.view.serverLn.addItems(value['serverPort'])
        self.view.workLn.addItems(value['workSpace'])
        self.view.userLn.addItems(value['user'])

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        actionA = QtWidgets.QAction('New Folder')
        actionB = QtWidgets.QAction('Delete Folder')
        actionC = QtWidgets.QAction('Import Unreal')
        if self.view.workTree.itemAt(pos):
            item = self.view.workTree.itemAt(pos)
            currentTreeItemPath = item.whatsThis(0)
            if os.path.isfile(currentTreeItemPath):
                contextMenuTree.addAction(actionC)
                actionC.triggered.connect(lambda: self.importAsset(self.view))
            contextMenuTree.addAction(actionA)
            contextMenuTree.addAction(actionB)
            actionA.triggered.connect(lambda: self.addFolder(self.view))
            actionB.triggered.connect(lambda: self.deleteFolder(self.view))
        contextMenuTree.exec_(QtGui.QCursor().pos())

    def showWorkListHandle(self, pos):
        contextMenuList = QtWidgets.QMenu()
        delAct = QtWidgets.QAction('Delete Item')
        if self.view.listview.itemAt(pos):
            contextMenuList.addAction(delAct)
            delAct.triggered.connect(lambda: self.__deleteItem(self.view))
        contextMenuList.exec_(QtGui.QCursor().pos())

    def checkedExportItem(self, item):
        if item.exportCheck.isChecked():
            item.exportType.setEnabled(True)
            item.exportPath.setEnabled(True)
        else:
            item.exportType.setEnabled(False)
            item.exportPath.setEnabled(False)

    def selectExportPath(self, item):
        outputPath = QtWidgets.QFileDialog.getExistingDirectory(item.parent,
                                                                u'选择输出FBX文件夹',
                                                                os.path.dirname(item.filePath))
        item.exportPath.exportDirectory = outputPath
        print(outputPath)
        print(item.fileBaseName.text())
        print(item.filePath)

    def addFolder(self, views):
        print(views)

    def deleteFolder(self, views):
        print(views)

    def importAsset(self, views):
        print(views)

    def __deleteItem(self, view):
        items = view.listview.selectedItems()
        for i in range(len(items)):
            itemNum = view.listview.row(items[i])
            item = view.listview.takeItem(itemNum)

    def setTreeWidget(self, clientRoot):
        self.view.workTree.clear()
        rootItem = QtWidgets.QTreeWidgetItem(self.view.workTree)
        rootItem.setText(0, os.path.basename(clientRoot))

        first_no = 10
        cmd_files = 'p4 files -i ' + clientRoot + '...'
        res_files = subprocess.getoutput(cmd_files)
        res_files = res_files.split('\n')
        root_node = Leaf(clientRoot)
        for res in res_files:
            out = res.split(clientRoot)[-1].split('/')
            lines = list()
            for level in range(len(out)):
                if out[level]:
                    index = '/' + out[level]
                    lines.append(index)

            first_node = Leaf(lines[0])
            if first_node.name not in [child.name for child in root_node.children]:
                first_node.set_value(str(first_no))
                first_no = first_no + 1
                root_node.add_child(first_node)

            cur_node = root_node.search(first_node)
            for node in [Leaf(name=lines[tmp]) for tmp in range(1, len(lines))]:  # 二级以后直接根据一级目录的编号开始
                if node.name not in [child.name for child in cur_node.children]:
                    length = len(cur_node.children)
                    node.set_value(str(length + 100 * int(cur_node.value)))
                    cur_node.add_child(node)
                cur_node = root_node.search(node)
        data = root_node.to_json()

        # with open(os.path.dirname(os.path.dirname(__file__)) + '/temp/temp.json', 'w') as fp:
        #     import json
        #     json_data = json.dumps(data, indent=2)
        #     fp.write(json_data)
        #     fp.close()

        self.set_tree(rootItem, data)

    def set_tree(self, leaf, leafName):
        if leafName['children']:
            for child in leafName['children']:
                child_root = QtWidgets.QTreeWidgetItem(leaf)
                child_root.setText(0, os.path.basename(child['name']))
                self.set_tree(child_root, child)

    def callBack(self):
        self.appSetting.init()
        configValue = self.appSetting.getConfig()
        serverPort = self.view.serverLn.currentText()
        user = self.view.userLn.currentText()
        workSpace = self.view.workLn.currentText()
        if serverPort not in configValue['serverPort']:
            configValue['serverPort'].append(serverPort)
        if user not in configValue['user']:
            configValue['user'].append(user)
        if workSpace not in configValue['workSpace']:
            configValue['workSpace'].append(workSpace)
        self.appSetting.setConfig(configValue)