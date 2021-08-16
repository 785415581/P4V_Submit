import os
import re
import subprocess

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from Python.modules.app_setting import AppSetting
from Python.utils.Leaf import Leaf
from Python.utils.utils import Utils
from Python.utils import P4Utils


class AppFunction(object):

    def __init__(self):
        self.appSetting = AppSetting()
        self._view = None
        self._clientStream = None
        self._clientRoot = None
        self._validation = None

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    @property
    def clientStream(self):
        return self._clientStream

    @clientStream.setter
    def clientStream(self, clientStream):
        self._clientStream = clientStream

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, clientRoot):
        self._clientRoot = clientRoot

    @property
    def validation(self):
        return self._validation

    @validation.setter
    def validation(self, value):
        self._validation = value

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
        self.view.currentPathCombox.setCurrentText(self.clientStream)
        self.view.typeComboBox.clear()
        self.view.assetNameComboBox.clear()
        self.view.submitStepCom.clear()
        for i in Utils.listdir(self.clientStream):
            self.view.typeComboBox.addItem(i, "{}/{}".format(self.clientStream, i))

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
        if value['password']:
            self.view.passwordLn.setText(value['password'][0])

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        actionA = QtWidgets.QAction('New Folder')
        actionB = QtWidgets.QAction('Delete Folder')
        actionC = QtWidgets.QAction('Sync to local')
        # actionC.setDisabled(True)
        if self.view.workTree.itemAt(pos):
            item = self.view.workTree.itemAt(pos)
            # currentTreeItemPath = item.whatsThis(0)
            # if os.path.isfile(currentTreeItemPath):
            #     contextMenuTree.addAction(actionC)

            contextMenuTree.addAction(actionA)
            contextMenuTree.addAction(actionB)
            contextMenuTree.addAction(actionC)
            actionA.triggered.connect(lambda: self.addFolder(self.view))
            actionB.triggered.connect(lambda: self.deleteFolder(self.view))
            actionC.triggered.connect(lambda: self.syncFile(self.view))
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

    def syncFile(self, view):
        items = view.workTree.selectedItems()
        self.validation()
        for item in items:
            p4Path = item.whatsThis(0)
            if re.findall(r'#\d+(.*?)[)]', p4Path):
                p4Path = re.sub(r'#\d+(.*?)[)]', str(), p4Path).replace('\\', '/')
                P4Utils.syncFile(p4Path)
            else:
                p4Path = p4Path + '/...'
                P4Utils.syncFile(p4Path)

    def __deleteItem(self, view):
        items = view.listview.selectedItems()
        for i in range(len(items)):
            itemNum = view.listview.row(items[i])
            item = view.listview.takeItem(itemNum)

    def setTreeWidget(self, clientStream):
        self.view.workTree.clear()
        first_no = 10
        cmd_files = 'p4 files -i ' + clientStream + '...'
        res_files = subprocess.getoutput(cmd_files)
        res_files = res_files.split('\n')
        root_node = Leaf(clientStream)
        for res in res_files:
            if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
                continue
            out = res.split(clientStream)[-1].split('/')
            temp = list()
            level = str()
            for index in range(len(out)):
                if out[index]:
                    level = level + '/' + out[index]
                    temp.append(level)
            lines = temp
            first_node = Leaf(lines[0])
            if first_node.name not in [child.name for child in root_node.children]:
                first_node.set_value(str(first_no))
                first_node.set_fullPath("{}{}".format(clientStream, first_node.name))
                first_no = first_no + 1
                root_node.add_child(first_node)

            cur_node = root_node.search(first_node)
            for node in [Leaf(name=lines[tmp]) for tmp in range(1, len(lines))]:
                if node.name not in [child.name for child in cur_node.children]:
                    length = len(cur_node.children)
                    node.set_value(str(length + 100 * int(cur_node.value)))
                    node.set_fullPath("{}{}".format(clientStream, node.name))
                    cur_node.add_child(node)
                cur_node = root_node.search(node)
        data = root_node.to_json()

        # with open(os.path.dirname(os.path.dirname(__file__)) + '/temp/temp.json', 'w') as fp:
        #     import json
        #     json_data = json.dumps(data, indent=2)
        #     fp.write(json_data)
        #     fp.close()
        rootItem = QtWidgets.QTreeWidgetItem(self.view.workTree)
        rootItem.setWhatsThis(0, clientStream)
        rootItem.setText(0, os.path.basename(clientStream))
        self.set_tree(rootItem, data)
        self.view.workTree.setSortingEnabled(True)
        self.view.workTree.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def set_tree(self, leaf, leafName):
        if leafName['children']:
            for child in leafName['children']:
                child_root = QtWidgets.QTreeWidgetItem(leaf)

                child_root.setWhatsThis(0, child['path'])
                child_root.setText(0, os.path.basename(child['name']))
                self.set_tree(child_root, child)

    def showPassword(self):
        self.view.passwordBtn.setStyleSheet("""QPushButton {
        min-width:10px;
        background-color: rgba(0, 0, 0, 0);
        background-position: center;
        background-repeat: no-repeat;
        background-image: url(:/icons/icons/display_password.png);}""")
        self.view.passwordLn.setEchoMode(QtWidgets.QLineEdit.Normal)

    def hidePassword(self):
        self.view.passwordBtn.setStyleSheet("""QPushButton {
        min-width:10px;
        background-color: rgba(0, 0, 0, 0);
        background-position: center;
        background-repeat: no-repeat;
        background-image: url(:/icons/icons/no_display_password.png);}""")
        self.view.passwordLn.setEchoMode(QtWidgets.QLineEdit.Password)

    def callBack(self):
        self.appSetting.init()
        configValue = self.appSetting.getConfig()
        serverPort = self.view.serverLn.currentText()
        user = self.view.userLn.currentText()
        workSpace = self.view.workLn.currentText()
        password = self.view.passwordLn.text()
        if serverPort not in configValue['serverPort']:
            configValue['serverPort'].append(serverPort)
        if user not in configValue['user']:
            configValue['user'].append(user)
        if workSpace not in configValue['workSpace']:
            configValue['workSpace'].append(workSpace)
        if password not in configValue['password']:
            configValue['password'].append(password)
        self.appSetting.setConfig(configValue)
