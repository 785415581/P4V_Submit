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
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from P4Module.p4_module import P4Client
import AssetBrowser.modules.app_utils as app_utils
from AssetBrowser.modules.extension import DialogAddLabel_UI
from AssetBrowser.modules.ImportFunction import unrealFunctions
import importlib

importlib.reload(unrealFunctions)
importlib.reload(DialogAddLabel_UI)


class AddLabels(QtWidgets.QDialog, DialogAddLabel_UI.Ui_Dialog):
    def __init__(self):
        super(AddLabels, self).__init__()

        self.itemLabels = None
        self._select_file = None
        self._kwargs = None
        self._configData = None
        self.setupUi(self)
        self.columnView = self.levelColumnView
        # self.columnView.enterEvent = self.enter_event
        self.columnView.setColumnWidths([20, 20, 20])
        self.columnView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.columnView.customContextMenuRequested.connect(lambda: self.showContextMenu(self.columnView))
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
        for filePath, info in itemInfo.items():
            item = QtWidgets.QListWidgetItem()
            item.setText(os.path.basename(filePath))
            item.setData(QtCore.Qt.UserRole, info)
            self.itemListWidget.addItem(item)

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
        index = columnView.currentIndex()
        container = list()
        container = self.getAllSelectColumnItem(index, container)
        count = columnView.model().columnCount(index)
        text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', u'输入子文件夹名称')
        if ok:
            item = columnView.model().itemFromIndex(index)
            container.reverse()
            lens = self.getChildIndex(container, self.configData)
            subItem = QtGui.QStandardItem(text)
            item.setChild(lens, 0, subItem)
            item.parent().appendRow(subItem)
            container.append(text)
            self.configData = self.feedbackConfig(container, self.configData)
            # from pprint import pprint
            # pprint(configData)
        # print(item.parent(), item.parent().text())
        # print(columnView.currentIndex().parent().row())

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
        for index in range(self.itemListWidget.count()):
            item = self.itemListWidget.item(index)
            data = item.data(QtCore.Qt.UserRole)
            localPath = data.get("localPath", "")
            severPath = data.get("serverPath", "")
            if localPath.split('.')[-1] != self.kwargs.get('ext'):
                app_utils.add_log("Invalid file format...{}".format(localPath))
                continue
            labels = self.getLabelsFromLayout()
            unrealPath = self.setLabelsCombineUnrealPath(labels)
            self.UnrealObj = self.kwargs.get("obj")
            self.UnrealObj.asset = data.get("asset", "")
            self.UnrealObj.type = data.get("type", "")
            self.UnrealObj.step = data.get("step", "")
            self.p4Model = data.get("p4Model", "")
            if unrealPath:
                if self.UnrealObj.step:
                    unrealPath = "/Game/" + unrealPath + "/" + self.UnrealObj.asset + "/" + self.UnrealObj.step
                else:
                    unrealPath = "/Game/" + unrealPath
            else:
                unrealPath = "/Game/Resource/" + self.UnrealObj.type + "/" + self.UnrealObj.asset+"/" + self.UnrealObj.step

            destination_path = self.UnrealObj.init_destination_path(default=unrealPath)
            if "" in unrealPath.split('/')[1::]:
                QtWidgets.QMessageBox.warning(self, "Waring", "Invalid path", QtWidgets.QMessageBox.Ok)
                return
            destination_name = self.UnrealObj.init_destination_name()
            options = self.UnrealObj.build_static_mesh_import_options()
            importTask = self.UnrealObj.creatImportTask(localPath, destination_path, destination_name, options)
            self.UnrealObj.execute_import_tasks(importTask)
            self.feedbackTag(self.p4Model, unrealPath, data)
        self.feedbackConfigData()
        self.close()

    def feedbackConfigData(self):

        try:
            with open(os.path.dirname(__file__) + '/FileStructure.json', 'w') as fd:
                json.dump(self.configData, fd, indent=2, sort_keys=1)
                fd.close()
        except IOError:
            traceback.print_exc()

    def feedbackTag(self, p4Model, unrealPath, data):
        if not unrealPath:
            return
        labels = unrealPath.split('/')[1::]
        labels.remove('Game')
        labels.remove(data.get("step", ""))
        labels.remove(data.get("asset", ""))
        old_labels = p4Model.getFileLabels(data.get("localPath"))
        for label in old_labels:
            if label:
                p4Model.changeLabelOwner(label, p4Model.user)
                p4Model.deleteFileLabels(data.get("localPath"), label)

        for label in labels:
            if label:
                p4Model.addFileLabels(data.get("localPath"), label)

    def setColumnItemSelect(self, index):
        self.__clearLabel()
        container = list()
        container = self.getAllSelectColumnItem(index, container)
        self.itemLabels = container
        items = self.itemListWidget.selectedItems()
        for item in items:
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
        for i in range(labelCount, -1, -1):
            label = self.verticalLayout.itemAt(i)
            if label is not None:
                label = label.widget()
                labels.append(label.text())
        return labels

    def setLabelsCombineUnrealPath(self, labels):

        for label in labels:
            router = []
            if label not in self.configData:
                index = str()
                for level in range(len(labels)):
                    if labels[level]:
                        if level == 0:
                            index = labels[level]
                            router.append(index)
                        else:
                            index = index + '/' + labels[level]
                            router.append(index)
                return max(router)
            else:
                for label in labels:
                    router = []
                    result = self.find_by_exhaustion(label, self.configData, router)
                    if result:
                        index = str()
                        for level in range(len(result[1])):
                            if result[1][level]:
                                if level == 0:
                                    index = result[1][level]
                                    router.append(index)
                                else:
                                    index = index + '/' + result[1][level]
                                    router.append(index)
            return max(router)

    def find_by_exhaustion(self, input_key, current_dict, router):
        '''
        :param input_key:  the key you given
        :param current_dict: the dict you have to scan
        :param router: record your route to reach here
        :return:
        '''

        router = copy.deepcopy(router)
        for index, key in enumerate(current_dict):
            val = current_dict.get(key)
            if input_key == key:
                router.append(key)
                return val, router
            elif isinstance(val, dict):
                router.append(key)
                result_tuple = self.find_by_exhaustion(input_key, val, router)
                if result_tuple:
                    return result_tuple[0], result_tuple[1]
                else:
                    if router:
                        router = router[0:len(router) - 1]

    def randomColor(self):
        colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return "#" + color


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AddLabels()
    # labels = ['Game', 'Character']
    # unrealPath = window.setLabelsCombineUnrealPath(labels)
    # print(unrealPath)
    window.initUI()
    window.show()
    app.exec_()