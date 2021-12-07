#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/3 11:21
"""
import os
import sys
import json
import copy
import random
import traceback
import importlib
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from P4Module.p4_module import P4Client
import AssetBrowser.modules.app_utils as app_utils
from AssetBrowser.modules.extension import DialogAddLabel_UI

# from AssetBrowser.modules.ImportFunction import unrealFunctions
# importlib.reload(unrealFunctions)

importlib.reload(DialogAddLabel_UI)


class AddLabels(QtWidgets.QDialog, DialogAddLabel_UI.Ui_Dialog):
    def __init__(self):
        super(AddLabels, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.itemLabels = None
        self._select_file = None
        self._kwargs = None
        self._configData = None
        self.jsonPathList = list()
        self.setupUi(self)
        self.columnView = self.levelColumnView
        # self.columnView.enterEvent = self.enter_event
        self.columnView.setColumnWidths([20, 20, 20])
        self.columnView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.columnView.customContextMenuRequested.connect(self.showContextMenu)
        self.initSignal()

    def enter_event(self, event):
        print('2222')

    @property
    def selectFiles(self):
        return self._select_file

    @selectFiles.setter
    def selectFiles(self, value):
        self._select_file = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    @property
    def configData(self):
        return self._configData

    @configData.setter
    def configData(self, value):
        self._configData = value

    def initUI(self):
        model = QtGui.QStandardItemModel()
        with open(os.path.dirname(__file__) + '/FileStructure.json') as fp:
            data = json.load(fp)
        self.configData = data
        self.setData(self.configData, model)
        self.columnView.setModel(model)

    def initSignal(self):
        self.itemListWidget.itemClicked.connect(self.setDisplayLabel)
        self.columnView.clicked.connect(self.setColumnItemSelect)
        self.columnView.doubleClicked.connect(self.setConfigData)
        self.okBtn.clicked.connect(self.setImportOption)
        self.cancelBtn.clicked.connect(self.close)

    def setDisplayLabel(self, item):
        self.__clearLabel()
        data = item.data(QtCore.Qt.UserRole)
        labels = data.get("labels", "")

        for label in labels:
            obj = QtWidgets.QLabel()
            obj.setText(label)
            obj.setStyleSheet("background-color:%s" % self.randomColor())
            self.verticalLayout.insertWidget(-1, obj)

    def addFileItem(self, itemInfo):
        itemList = list()
        for filePath, info in itemInfo.items():
            item = QtWidgets.QListWidgetItem()
            item.setText(os.path.basename(filePath))
            item.setData(QtCore.Qt.UserRole, info)
            self.itemListWidget.addItem(item)
            itemList.append(item)
        self.setDisplayLabel(itemList[0])

    def setData(self, data, parentItem):
        for group, value in data.items():
            subItem = QtGui.QStandardItem(group)
            parentItem.appendRow(subItem)
            self.setData(value, subItem)

    def showContextMenu(self, columnView):
        columnView.contextMenu = QtWidgets.QMenu()
        actionA = columnView.contextMenu.addAction(u'Add Item...')
        columnView.contextMenu.popup(QtGui.QCursor.pos())
        actionA.triggered.connect(lambda: self.actionHandler(columnView))
        columnView.contextMenu.show()

    def setConfigData(self, index):
        print(index)

    def actionHandler(self, columnView):
        # ToDo: add label
        index = self.columnView.currentIndex()
        container = list()
        container = self.getAllSelectColumnItem(index, container)
        count = self.columnView.model().columnCount(index)
        text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', u'输入子文件夹名称')
        if ok:
            item = self.columnView.model().itemFromIndex(index)
            container.reverse()
            lens = self.getChildIndex(container, self.configData)
            subItem = QtGui.QStandardItem(text)
            item.setChild(lens, 0, subItem)
            item.parent().appendRow(subItem)
            container.append(text)
            self.configData = self.feedbackConfig(container, self.configData)

    def getChildIndex(self, container, configData):
        lens = None
        for label in container:
            if label in configData:
                lens = len(configData[label])
                configData = configData[label]
        return lens

    def feedbackConfig(self, container, configData):

        for label in container:
            if label in configData:
                container.remove(label)
                self.feedbackConfig(container, configData[label])
            else:
                configData.update({label: {}})

        return configData

    def setImportOption(self):
        self.close()
        for index in range(self.itemListWidget.count()):
            item = self.itemListWidget.item(index)
            data = item.data(QtCore.Qt.UserRole)
            localPath = data.get("localPath", "")
            if localPath.split('.')[-1] != self.kwargs.get('ext'):
                app_utils.add_log("Invalid file format...{}".format(localPath))
                continue
            labels = self.getLabelsFromLayout()
            if not labels:
                labels = self.kwargs.get("labels")
            unrealPath = self.setLabelsCombineUnrealPath(labels)
            if not labels:
                unrealPath = None
            self.UnrealObj = self.kwargs.get("obj")
            self.UnrealObj.asset = data.get("asset", "")
            self.UnrealObj.type = data.get("type", "")
            self.UnrealObj.step = data.get("step", "")
            self.p4Model = data.get("p4Model", "")
            if '/' in self.UnrealObj.asset:
                self.UnrealObj.asset = self.UnrealObj.asset.split('/')[-1]

            if unrealPath:
                unrealPath = "/Game" + unrealPath
            else:
                unrealPath = "/Game/" + self.UnrealObj.type + "/" + self.UnrealObj.asset
            destination_path = self.UnrealObj.init_destination_path(default=unrealPath)
            if "" in unrealPath.split('/')[1::]:
                QtWidgets.QMessageBox.warning(self, "Waring", "Invalid path", QtWidgets.QMessageBox.Ok)
                return
            destination_name = self.UnrealObj.init_destination_name()
            options = self.UnrealObj.build_static_mesh_import_options()
            importTask = self.UnrealObj.creatImportTask(localPath, destination_path, destination_name, options)
            self.UnrealObj.execute_import_tasks(importTask)
            self.feedbackTag(self.p4Model, labels, data)
        self.feedbackConfigData()


    def feedbackConfigData(self):

        try:
            with open(os.path.dirname(__file__) + '/FileStructure.json', 'w') as fd:
                json.dump(self.configData, fd, indent=2, sort_keys=1)
                fd.close()
        except IOError:
            traceback.print_exc()

    def feedbackTag(self, p4Model, labels, data):
        old_labels = p4Model.getFileLabels(data.get("localPath"))
        for label in old_labels:
            p4Model.changeLabelOwner(label, p4Model.user)
            p4Model.deleteFileLabels(data.get("localPath"), label)

        for label in labels:
            p4Model.changeLabelOwner(label, p4Model.user)
            p4Model.addFileLabels(data.get("localPath"), label)
            p4Model.cleanLabelView(label)

    def setColumnItemSelect(self, index):
        self.__clearLabel()
        container = list()
        container = self.getAllSelectColumnItem(index, container)
        self.itemLabels = container
        itemCount = self.itemListWidget.count()
        if itemCount:
            for index in range(itemCount):
                item = self.itemListWidget.item(index)
                data = item.data(QtCore.Qt.UserRole)
                data.update({"labels": container})
                item.setData(QtCore.Qt.UserRole, data)
            for label in container:
                obj = QtWidgets.QLabel()
                obj.setText(label)
                obj.setStyleSheet("background-color:%s" % self.randomColor())
                self.verticalLayout.insertWidget(-1, obj)

    def __clearLabel(self):
        labelCount = self.verticalLayout.count()
        for i in range(labelCount, -1, -1):
            label = self.verticalLayout.itemAt(i)
            if label is not None:
                label.widget().deleteLater()
                self.verticalLayout.removeItem(label)

    def getAllSelectColumnItem(self, index, container):
        if index.parent().row() > -1:
            label = index.data()
            container.append(label)
            self.getAllSelectColumnItem(index.parent(), container)
        else:
            container.append(index.data())
        return container

    def getLabelsFromLayout(self):
        labels = list()
        labelCount = self.verticalLayout.count()
        if not labelCount:
            return None
        for i in range(labelCount, -1, -1):
            label = self.verticalLayout.itemAt(i)
            if label is not None:
                label = label.widget()
                labels.append(label.text())
        return labels

    def setLabelsCombineUnrealPath(self, labels):
        self.resJsonPath(self.configData, path='')
        if self.jsonPathList:
            for jsonPath in self.jsonPathList:
                if set(jsonPath.strip('/').split('/')) == set(labels):
                    self.jsonPathList = list()
                    return jsonPath

    def resJsonPath(self, pathJson, path=''):
        for key, value in pathJson.items():
            if value:
                cycPath = path + '/' + key
                self.resJsonPath(value, cycPath)
            else:
                realPath = path + "/"+key
                self.jsonPathList.append(realPath)

    def randomColor(self):
        colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return "#" + color


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AddLabels()
    labels = ['Character',  'Male', 'Gloves', 'Texture']
    window.initUI()
    unrealPath = window.setLabelsCombineUnrealPath(labels)
    print(unrealPath)
    # window.show()
    # app.exec_()
