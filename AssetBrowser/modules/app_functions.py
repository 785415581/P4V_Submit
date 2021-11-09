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
import AssetBrowser.utils.moveFile as moveFile

import AssetBrowser.modules.ImportFunction.startImport as startImport
import AssetBrowser.modules.ExportFunction.startExport as startExport

import AssetBrowser.modules.publish_hooks.startPublish as startPublish

import AssetBrowser.view.baseWidget as baseWidget

import imp

imp.reload(app_setting)
imp.reload(global_setting)
imp.reload(Leaf)
imp.reload(utils)

imp.reload(startImport)
imp.reload(startExport)
imp.reload(moveFile)
imp.reload(startPublish)
imp.reload(baseWidget)
import tempfile
import shutil
from functools import partial


class AppFunc():
    def __init__(self):
        self.appSetting = app_setting.AppSetting()
        self.appSetting.init()
        self._view = None
        self._clientStream = None
        self._clientRoot = None
        self._validation = None
        self.p4Model = None
        self.currentPathList = []

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

        self.view.typeComboBox.addItems(list(self.data_dict.keys()))
        for default_type in global_setting.ASSETTYPE:
            if default_type not in self.data_dict.keys():
                self.view.typeComboBox.addItem(default_type)

        self.view.submitStepCom.addItems(global_setting.STEP)

        current_type = self.view.typeComboBox.currentText()
        if current_type in self.data_dict:
            self.view.assetNameComboBox.addItems(list(self.data_dict[current_type].keys()))

    def changeType(self, index):
        print("change type")

        self.view.assetNameComboBox.clear()
        currentType = self.view.typeComboBox.currentText()
        if currentType not in self.data_dict:
            return

        self.view.assetNameComboBox.addItems(list(self.data_dict[currentType].keys()))
        self.setTreeWidget()

    def changeAsset(self, index):
        print("change asset")
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
            first_password = list(value["users"].values())[0]
        else:
            first_user = self.p4Model.user
            first_password = self.p4Model.password

        self.view.userLn.insertItem(0, first_user)
        self.view.userLn.setCurrentIndex(0)
        self.view.passwordLn.setText(first_password)

    def showWorkTreeHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()
        # actionC.setDisabled(True)
        print("run")
        current_item = self.view.listWidget.itemAt(pos)
        actionNew = None
        actionDel = None
        if not current_item:

            actionNew = QtWidgets.QAction('New Folder')

            parent_item = current_item

        else:
            if not ("." in current_item.text(0) and (not current_item.childItems)):
                actionNew = QtWidgets.QAction('New Folder')
            actionDel = QtWidgets.QAction('Delete')
            parent_item = self.view.listWidget

        if actionNew:
            contextMenuTree.addAction(actionNew)
            actionNew.triggered.connect(partial(self.addFolder, parent_item))
        if actionDel:
            contextMenuTree.addAction(actionDel)
            actionDel.triggered.connect(partial(self.deleteItems, parent_item))

        contextMenuTree.exec_(QtGui.QCursor().pos())

    def showHistoryHandle(self, pos):
        contextMenuTree = QtWidgets.QMenu()

        row = self.view.history_list.rowAt(pos.y())
        data = self.view.history_list.model().itemData(self.view.history_list.model().index(row, 0))
        if data:
            actionNew = QtWidgets.QAction('Get This Resivion')
            contextMenuTree.addAction(actionNew)
            actionNew.triggered.connect(lambda: self.change_version(data))

        contextMenuTree.exec_(QtGui.QCursor().pos())

    def add_log(self, log_text, w=False, e=False):
        logText = utils.Utils.colorText(log_text, w, e)
        self.view.log_edit.appendHtml(logText)

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

    def addFolder(self, parent_item):
        source_path = "/NewFolder"
        if isinstance(parent_item, baseWidget.PathTreeItem):
            source_path = parent_item.source_path + source_path
        baseWidget.PathTreeItem(source_path, parent=parent_item)

    def deleteItems(self, parent_item):
        print(parent_item)
        # index = self.view.listWidget.indexFromItem(current_item)
        # self.view.listWidget.takeTopLevelItem(index)

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
        # print(self.full_file_dict)
        if data_key not in self.full_file_dict:
            return

        tree_data_dict = {}
        max_length = 0
        for half_index in range(len(self.full_file_dict[data_key])):
            full_path = self.full_file_dict[data_key][half_index]
            half_path = self.half_file_dict[full_path]
            names = half_path.split('/')
            temp = list()
            level = str()

            for name_index in range(len(names)):
                if names[name_index]:
                    level = level + '/' + names[name_index]
                    temp.append(level)
            max_length = max(max_length, len(temp))
            tree_data_dict[full_path] = temp
        # print(tree_data_dict)
        # import json
        # with open("D:/chenghh/test.json", "w") as wf:
        #     json.dump(tree_data_dict, wf, indent=4)

        for matrix_index in range(max_length):
            level_items = {}

            for server_file, levels in tree_data_dict.items():
                if matrix_index >= len(levels):
                    continue

                current_path = server_file.split(levels[matrix_index])[0] + levels[matrix_index]
                if current_path not in level_items:
                    if matrix_index > 0:
                        parent = levels[matrix_index - 1]
                    else:
                        parent = self.view.workTree

                    item = baseWidget.PathTreeItem(current_path, source_model="server", parent=parent)
                    level_items[current_path] = item
                    levels[matrix_index] = item
                    if (matrix_index == len(levels) - 1) and server_file in self.p4_file_infos:
                        if self.p4_file_infos[server_file]["haveRev"]:
                            label = QtWidgets.QLabel(self.p4_file_infos[server_file]["haveRev"])
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.view.workTree.setItemWidget(item, 1, label)
                            item.have_rev = self.p4_file_infos[server_file]["haveRev"]

                        if self.p4_file_infos[server_file]["headRev"]:
                            label = QtWidgets.QLabel(self.p4_file_infos[server_file]["headRev"])
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.view.workTree.setItemWidget(item, 2, label)

                else:
                    levels[matrix_index] = level_items[current_path]

        self.view.workTree.setSortingEnabled(True)
        self.view.workTree.sortByColumn(0, QtCore.Qt.AscendingOrder)
        if self.view.extend.isChecked():
            self.view.workTree.expandAll()

    def listPath(self, item):
        half_path = item.half_path
        servePre, localPre = self.getPathPre()

        res = servePre + half_path
        if self.clientRoot and res not in self.currentPathList:
            self.view.currentPathCombox.addItem(res.replace('\\', '/'))
            self.currentPathList.append(res)
            index = self.view.currentPathCombox.count()
            self.view.currentPathCombox.setItemData(index - 1, item, QtCore.Qt.UserRole)
        self.view.currentPathCombox.setCurrentText(res.replace('\\', '/'))

        if self.view.show_history.isChecked():
            version_list = self.p4Model.getVersions(item.source_path)
            self.view.history_list.history_parent = item
            self.view.history_list.model().setData(list(version_list))
        else:
            self.view.history_list.model().setData(list())

    def change_version(self, item_data):
        version = item_data[0]

        sel_item = self.view.history_list.history_parent
        if not sel_item:
            print("No Asset select")
            return

        if sel_item.source_path in self.p4_file_infos:
            self.p4Model.syncFile(sel_item.source_path, version=str(version))
            self.p4_file_infos[sel_item.source_path]["haveRev"] = str(version)
            sel_item.have_rev = str(version)

        label = QtWidgets.QLabel(version)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.view.workTree.setItemWidget(sel_item, 1, label)

    def printTest(self, item):
        print(item.source_path)

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
            self.add_log(u"Warning:未选择文件", w=True)
            return

        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()

        servePrePublish, localPrePublish = self.getPathPre()
        # servePreWork, localPreWork = self.getPathPre("private")
        fileInfo = dict()
        for item in sel_items:
            half_path = item.half_path.replace('\\', '/')
            local_pub_path = localPrePublish + half_path

            if local_pub_path:
                # sync local version first
                self.p4Model.syncFile(local_pub_path, version=item.have_rev)
                fileLabel = self.p4Model.getFileLabels(local_pub_path)
                # #copy to private fold
                # local_work_path = localPreWork + half_path
                # moveFile.moveImportFile(local_pub_path, local_work_path)

                fileInfo[local_pub_path] = {}
                fileInfo[local_pub_path]['localPath'] = local_pub_path
                fileInfo[local_pub_path]['serverPath'] = servePrePublish + half_path
                fileInfo[local_pub_path]['type'] = current_type
                fileInfo[local_pub_path]['asset'] = current_asset
                fileInfo[local_pub_path]['step'] = current_step
                fileInfo[local_pub_path]['labels'] = fileLabel

                # start import
                log, result = startImport.start_import(model, local_pub_path, fileInfo=fileInfo)
                if result:
                    self.add_log(log)
                else:
                    self.add_log(log, e=True)

        return "", True

    def Export_btn_clicked(self, model):
        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()

        if model == "ExportScene":

            publish_temp_fold = os.path.join(tempfile.tempdir, "publish_temp")
            if not os.path.exists(publish_temp_fold):
                os.mkdir(publish_temp_fold)
            export_fold = tempfile.mkdtemp(dir=publish_temp_fold)
            log, result = startExport.start_export(current_type, current_asset, current_step, export_fold)

            if result:
                self.add_log(log)
                # self.view.listWidget.clear()
                for sub in os.listdir(export_fold):
                    self.view.listWidget.createItem(os.path.join(export_fold, sub), source_model="export")
            else:
                self.add_log(log, e=True)
                shutil.rmtree(export_fold)



        elif model == "Publish":
            comment_log = self.view.textEdit.toPlainText()
            servePre, localPre = self.getPathPre()
            iter = QtWidgets.QTreeWidgetItemIterator(self.view.listWidget)
            dst_files = []
            while iter.value():
                item = iter.value()
                source_path = item.source_path
                source_model = item.source_model
                have_rev = item.have_rev
                dst_path = localPre + item.half_path
                moveFile.movePublishFile(source_path, dst_path, source_model, have_rev, self.p4Model)
                dst_files.append(dst_path)
                iter = iter.__iadd__(1)

            log, result = startPublish.startPublish(dst_files, p4model=self.p4Model, log=comment_log)
            if result:
                self.add_log(log)

            else:
                self.add_log(log, e=True)
            self.view.listWidget.clear()

    def getPathPre(self, area="publish"):
        current_type = self.view.typeComboBox.currentText()
        current_asset = self.view.assetNameComboBox.currentText()
        current_step = self.view.submitStepCom.currentText()
        client_info_dict = self.p4Model.getClienInfo()
        client_root = client_info_dict["clientRoot"]
        client_stream = client_info_dict["clientStream"]
        servePre = utils.Utils.getPathPre(client_stream, current_type, current_asset, current_step, area)
        workPre = utils.Utils.getPathPre(client_root, current_type, current_asset, current_step, area)

        return servePre.replace("\\", "/"), workPre.replace("\\", "/")

    def callBack(self):
        self.appSetting.init()
        configValue = self.appSetting.getConfig()
        # serverPort = self.view.serverLn.currentText()
        user = self.view.userLn.currentText()
        # workSpace = self.view.workLn.currentText()
        password = self.view.passwordLn.text()

        # if serverPort not in configValue['serverPort']:
        #     configValue['serverPort'].append(serverPort)

        configValue.setdefault("users", {})[user] = password

        self.appSetting.setConfig(configValue)
