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
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from P4Module.p4_module import P4Client
from AssetBrowser.modules.extension import DialogAddLabel_UI

import importlib

importlib.reload(DialogAddLabel_UI)


class AddLabels(QtWidgets.QDialog, DialogAddLabel_UI.Ui_Dialog):
    def __init__(self):
        super(AddLabels, self).__init__()

        self.itemLabels = None
        self._select_file = None
        self._kwargs = None

        self.setupUi(self)
        self.columnView = self.levelColumnView
        self.columnView.setColumnWidths([20, 20, 20])
        self.columnView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.columnView.customContextMenuRequested.connect(lambda: self.showContextMenu(self.columnView))
        self.initSignal()

    @property
    def selectFile(self):
        return self._select_file

    @selectFile.setter
    def selectFile(self, value):
        self._select_file = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    def initUI(self):
        model = QtGui.QStandardItemModel()
        with open(os.path.dirname(__file__) + '/FileStructure.json') as fp:
            data = json.load(fp)
        self.setData(data, model)
        self.columnView.setModel(model)

    def initSignal(self):
        self.itemListWidget.itemClicked.connect(self.setDisplayLabel)
        self.columnView.clicked.connect(self.setColumnItemSelect)
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

    def actionHandler(self, columnView):
        item = columnView.model().itemFromIndex(columnView.currentIndex())
        subItem = QtGui.QStandardItem('rrrr')
        item.parent().appendRow(subItem)
        print(item.parent(), item.parent().text())
        print(columnView.currentIndex().parent().row())
        print("成功")

    def stepOption(self):
        pass

    def setImportOption(self):
        for index in range(self.itemListWidget.count()):
            item = self.itemListWidget.item(index)
            data = item.data(QtCore.Qt.UserRole)
            localPath = data.get("localPath", "")
            severPath = data.get("serverPath", "")

            labels = self.getLabelsFromLayout()
            unrealPath = self.setLabelsCombineUnrealPath(labels)

            self.UnrealObj = self.kwargs.get("obj")
            self.UnrealObj.asset = data.get("asset", "")
            self.UnrealObj.type = data.get("type", "")
            self.UnrealObj.step = data.get("step", "")
            if self.UnrealObj.step:
                unrealPath = "/Game/" + unrealPath + "/" + self.UnrealObj.step
            else:
                unrealPath = "/Game/" + unrealPath
            destination_path = self.UnrealObj.init_destination_path(default=unrealPath)
            if "" in unrealPath.split('/')[1::]:
                QtWidgets.QMessageBox.warning(self, "Waring", "Invalid path", QtWidgets.QMessageBox.Ok)
                return
            destination_name = self.UnrealObj.init_destination_name()
            options = self.UnrealObj.build_static_mesh_import_options()
            importTask = self.UnrealObj.creatImportTask(self.selectFile, destination_path, destination_name, options)
            self.UnrealObj.execute_import_tasks(importTask)
            self.feedbackTag(unrealPath, data)

            self.close()

    def feedbackTag(self, unrealPath, data):
        labels = unrealPath.split('/')[1::]
        labels.remove('Game')
        labels.remove(data.get("step", ""))
        labels = list(set(labels).difference(set(data.get("labels", ""))))
        for label in labels:
            if label:
                P4Client.addFileLabels(data.get("localPath"), label)

    def setColumnItemSelect(self, index):
        self.__clearLabel()
        container = list()
        container = self.getAllSelectColumnItem(index, container)
        self.itemLabels = container
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
        with open(os.path.dirname(__file__) + '/FileStructure.json') as fp:
            data = json.load(fp)
        for label in labels:
            router = []
            if label not in data:
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
                    result = self.find_by_exhaustion(label, data, router)
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