# -*- coding: utf-8 -*-

import os
import re

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import AssetBrowser.modules.app_setting as app_setting
import AssetBrowser.modules.global_setting as global_setting
import AssetBrowser.utils.Leaf as Leaf
import AssetBrowser.utils.utils as utils
import AssetBrowser.utils.P4Utils as P4Utils
import AssetBrowser.modules.ImportFunction.startImport as startImport
import AssetBrowser.modules.ExportFunction.startExport as startExport

import imp
imp.reload(app_setting)
imp.reload(global_setting)
imp.reload(Leaf)
imp.reload(utils)
imp.reload(P4Utils)
imp.reload(startImport)
imp.reload(startExport)
import tempfile
import shutil

class AppFunc():
    def __init__(self):
        self.appSetting = app_setting.AppSetting()
        self.appSetting.init()
        self._view = None
        self._clientStream = None
        self._clientRoot = None
        self._validation = None
        self.p4Model = None
        self.currentPathList=[]
        self.select_files=[]

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
        # self.view.assetNameComboBox.blockSignals(True)
        self.view.currentPathCombox.setCurrentText(self.clientStream)
        self.view.typeComboBox.clear()
        self.view.assetNameComboBox.clear()
        self.view.submitStepCom.clear()

        self.p4_file_infos = self.p4Model.getFiles(self.clientStream)

        self.full_file_dict, self.half_file_dict, self.data_dict = utils.Utils().getAssetsData(self.p4_file_infos)

        self.view.typeComboBox.addItems(self.data_dict.keys())
        current_type = self.view.typeComboBox.currentText()
        self.view.assetNameComboBox.addItems(self.data_dict[current_type].keys())
        current_asset = self.view.assetNameComboBox.currentText()
        self.view.submitStepCom.addItems(global_setting.STEP)




    def changeType(self, index):
        print("change type")

        self.view.assetNameComboBox.clear()
        currentType = self.view.typeComboBox.currentText()
        if currentType not in self.data_dict:
            return

        self.view.assetNameComboBox.addItems(self.data_dict[currentType].keys())
        self.setTreeWidget()

    def changeAsset(self, index):
        print("change asset")
        #self.view.submitStepCom.clear()
        # current_type = self.view.typeComboBox.currentText()
        # # current_asset = self.view.assetNameComboBox.currentText()
        # if current_type not in self.data_dict:
        #     return
        # if current_asset not in self.data_dict[current_type]:
        #     return
        # self.view.submitStepCom.addItems(self.data_dict[current_type][current_asset])

        self.setTreeWidget()

    def changeStep(self, index):
        print("change step")

        self.setTreeWidget()

    def extendTree(self):
        if self.view.extend.isChecked():
            self.view.workTree.expandAll()
        else:
            self.view.workTree.collapseAll()

    def initUser(self):
        value = self.appSetting.getConfig()
        # self.view.serverLn.addItems(value['serverPort'])
        # self.view.workLn.addItems(value['workSpace'])
        if "users" in value and value["users"]:
            first_user = list(value["users"].keys())[0]
            first_passward = list(value["users"].values())[0]
        else:
            first_user = self.p4Model.user
            first_passward = self.p4Model.password


        self.view.userLn.insertItem(0, first_user)
        self.view.userLn.setCurrentIndex(0)
        self.view.passwordLn.setText(first_passward)

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        # actionC.setDisabled(True)
        print("run")
        current_item = self.view.listWidget.itemAt(pos)
        if current_item:
            actionA = QtWidgets.QAction('New Folder')
            actionB = QtWidgets.QAction('Delete Folder')
            actionC = QtWidgets.QAction('Sync to local')
            #todo wait to judge file or fold to show actionC
            # currentTreeItemPath = current_item.whatsThis(0)
            # print(currentTreeItemPath)

            # if os.path.isfile(currentTreeItemPath):
            #     contextMenuTree.addAction(actionC)
            # app = QtWidgets.QApplication.instance()
            # if app and 'maya' in app.applicationName().lower():
            #     actionD = QtWidgets.QAction('import file')
            #     contextMenuTree.addAction(actionD)
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
        if self.view.listWidget.itemAt(pos):
            contextMenuList.addAction(delAct)
            delAct.triggered.connect(lambda: self.__deleteItem(self.view))
        else:
            action_save = QtWidgets.QAction('save current scene')
            action_export = QtWidgets.QAction('export scene')
            contextMenuList.addAction(action_save)
            contextMenuList.addAction(action_export)
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
                                                                'select export fold',
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

    def setTreeWidget(self):
        self.view.workTree.clear()
        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()
        data_key = "{0}_{1}_{2}".format(current_type, current_asset, current_step)
        print(self.half_file_dict)
        if data_key not in self.half_file_dict:
            return

        root_nodes = []
        first_node=None

        for index in range(len(self.half_file_dict[data_key])):

            half_path = self.half_file_dict[data_key][index]
            full_path = self.full_file_dict[data_key][index]
            out = half_path.split('/')
            temp = list()
            level = str()

            for index in range(len(out)):
                if out[index]:
                    level = level + '/' + out[index]
                    temp.append(level)
            lines = temp


            if lines[0] not in [exist_node.name for exist_node in root_nodes]:
                first_node = Leaf.Leaf(lines[0])
                first_node.set_fullPath("halfPath:{0}".format(first_node.name))
                root_nodes.append(first_node)

            cur_node = first_node

            nodes = []
            for tmp in range(1, len(lines)):
                node = Leaf.Leaf(name=lines[tmp])
                node.set_fullPath("halfPath:{0}".format(lines[tmp]))
                nodes.append(node)
            for node in nodes:
                if node.name not in [child.name for child in cur_node.children]:
                    length = len(cur_node.children)
                    node.set_value(str(length + 100 * int(cur_node.value)))
                    cur_node.add_child(node)
                cur_node = first_node.search(node)


            cur_node.set_ser_ver(self.p4_file_infos[full_path]["headRev"])
            cur_node.set_local_ver(self.p4_file_infos[full_path]["haveRev"])

        rootItem = QtWidgets.QTreeWidgetItem(self.view.workTree)
        rootItem.setText(0, os.path.basename("..."))

        for first_node in root_nodes:

            self.set_tree(rootItem, first_node.to_json())

        self.view.workTree.setSortingEnabled(True)
        self.view.workTree.sortByColumn(0, QtCore.Qt.AscendingOrder)
        if self.view.extend.isChecked():
            self.view.workTree.expandAll()

    def set_tree(self, parent, leafName):
        parent.setFirstColumnSpanned(True)
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setWhatsThis(0, leafName['path'])
        item.setText(0, os.path.basename(leafName['name']))

        if leafName["ser_ver"]:
            # ver_item = QtWidgets.QTreeWidgetItem(parent)
            # print(child["ser_ver"])
            label = QtWidgets.QLabel(leafName["ser_ver"])
            label.setAlignment(QtCore.Qt.AlignCenter)
            parent.treeWidget().setItemWidget(item, 1, label)

        if leafName["local_ver"]:
            label = QtWidgets.QLabel(leafName["local_ver"])
            label.setAlignment(QtCore.Qt.AlignCenter)
            parent.treeWidget().setItemWidget(item, 2, label)
        if leafName['children']:
            for child in leafName['children']:
                self.set_tree(item, child)

    def listPath(self, item):
        half_path = self.getCurrentPath(item).replace('\\', '/')
        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()
        res = utils.Utils.getAssetPath(current_type, current_asset, current_step, half_path)
        if self.clientRoot and res not in self.currentPathList:
            self.view.currentPathCombox.addItem(res.replace('\\', '/'))
            self.currentPathList.append(res)
            index = self.view.currentPathCombox.count()
            self.view.currentPathCombox.setItemData(index - 1, item, QtCore.Qt.UserRole)
        self.view.currentPathCombox.setCurrentText(res.replace('\\', '/'))

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
            return strPath

    def printTest(self, item):
        print(item.whatsThis(0))

    def show_log(self):
        if self.view.show_log_check.isChecked():
            self.view.groupBox_log.setHidden(False)
        else:
            self.view.groupBox_log.setHidden(True)

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

    def Import_btn_clicked(self, model):
        print("{0} btn pressed".format(model))
        sel_items = self.view.workTree.selectedItems()
        if not sel_items:
            self.add_log(u"Warning:未选择文件",w=True)
            return

        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()

        for item in sel_items:
            half_path = self.getCurrentPath(item).replace('\\', '/')
            asset_depot_path = utils.Utils.getAssetPath(current_type, current_asset, current_step, half_path)
            local_path = self.p4_file_infos[asset_depot_path]["clientFile"]
            if local_path:
                log, result = startImport.start_import(model, local_path, current_step)
                if result:
                    self.add_log(log)
                else:
                    self.add_log(log, e=True)

    def Export_btn_clicked(self, model):

        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()

        if model == "ExportScene":
            export_fold = tempfile.mkdtemp()
            if not os.path.exists(export_fold):
                os.makedirs(export_fold)

            log, result = startExport.start_export(current_type, current_asset, current_step, export_fold)

            if result:
                self.add_log(log)
                self.view.listWidget.clear()
                self.view.listWidget.createItem(export_fold)
            else:
                self.add_log(log, e=True)
                shutil.rmtree(export_fold)



        elif model == "Publish":
            pass



    def add_log(self, log_text, w=False, e=False):
        logText = utils.Utils.colorText(log_text, w, e)
        self.view.log_edit.appendHtml(logText)


    def callBack(self):
        self.appSetting.init()
        configValue = self.appSetting.getConfig()
        # serverPort = self.view.serverLn.currentText()
        user = self.view.userLn.currentText()
        # workSpace = self.view.workLn.currentText()
        password = self.view.passwordLn.text()

        # if serverPort not in configValue['serverPort']:
        #     configValue['serverPort'].append(serverPort)

        configValue.setdefault("users", {})[user]=password

        self.appSetting.setConfig(configValue)

