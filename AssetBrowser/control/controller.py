# -*- coding: utf-8 -*-
import os
from PySide2 import QtCore, QtGui, QtWidgets

import AssetBrowser.modules.app_functions as app_functions
import P4Module.p4_module as p4_module
import AssetBrowser.utils.utils as utils
from AssetBrowser.modules import global_setting

import imp
imp.reload(app_functions)
imp.reload(p4_module)
imp.reload(utils)

from functools import partial


class AlignDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)


class Controller(QtCore.QObject):
    def __init__(self):
        super(Controller, self).__init__()
        self._view = None
        self._utils = utils.Utils()
        self._p4Model = p4_module.P4Client()
        self._appFunction = app_functions.AppFunc()
        self._appFunction.p4Model = self._p4Model

    @property
    def p4Model(self):
        return self._p4Model

    @property
    def appFunction(self):
        return self._appFunction

    @appFunction.setter
    def appFunction(self, value):
        self._appFunction = value

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    @property
    def utils(self):
        return self._utils

    def init(self):
        self.appFunction.view = self.view

        if self.get_env() == "Maya":
            self.view.exportBtn.setEnabled(True)
            self.view.exportBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.view.workTree.clear()
        self.view.workTree.setColumnCount(3)
        self.view.workTree.setHeaderLabels(["Files", "LocalVersion", "ServerVersion"])

        self.view.workTree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #self.view.listWidget.tree.clear()
        self.view.assets_file_list.clear()
        self.view.currentPathCombox.clear()
        self.view.typeComboBox.setEnabled(True)
        self.view.assetNameComboBox.setEnabled(True)

    def initUI(self):
        self.p4Model.user = self.view.userLn.currentText()
        self.p4Model.client = self.view.workLn.currentText()
        self.p4Model.serverPort = self.view.serverLn.currentText()

    def initSignal(self):
        self.view.workTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


        self.view.assets_file_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.passwordBtn.pressed.connect(self.appFunction.showPassword)
        self.view.passwordBtn.released.connect(self.appFunction.hidePassword)

        self.view.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.listWidget.customContextMenuRequested.connect(self.appFunction.showWorkTreeHandle)

        self.view.history_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.history_list.customContextMenuRequested.connect(self.appFunction.showHistoryHandle)

        self.view.workTree.itemClicked.connect(self.appFunction.listPath)
        self.view.listWidget.itemClicked.connect(self.appFunction.printTest)
        self.view.assets_file_list.customContextMenuRequested.connect(self.appFunction.showWorkListHandle)
        self.view.typeComboBox.currentIndexChanged.connect(self.appFunction.changeType)
        self.view.assetNameComboBox.currentTextChanged.connect(self.appFunction.changeAsset)
        self.view.submitStepCom.currentIndexChanged.connect(self.appFunction.changeStep)
        self.view.extend.stateChanged.connect(self.appFunction.extendTree)
        self.view.show_log_check.stateChanged.connect(self.appFunction.showLog)

        self.view.open_scene_button.clicked.connect(partial(self.appFunction.btnToolClicked, "OpenScene"))
        self.view.new_scene_button.clicked.connect(partial(self.appFunction.btnToolClicked, "NewScene"))
        self.view.save_scene_button.clicked.connect(partial(self.appFunction.btnToolClicked, "SaveScene"))
        self.view.import_subasset_button.clicked.connect(partial(self.appFunction.btnToolClicked, "importSubasset"))

        self.view.import_select_button.clicked.connect(partial(self.appFunction.btnImportClicked, "import"))
        self.view.reference_select_button.clicked.connect(partial(self.appFunction.btnImportClicked, "reference"))
        self.view.open_select_button.clicked.connect(partial(self.appFunction.btnImportClicked, "open"))
        self.view.down_select_button.clicked.connect(partial(self.appFunction.btnToolClicked, "down"))

        self.view.exportBtn.clicked.connect(partial(self.appFunction.btnExportClicked, "ExportScene"))
        self.view.exportBtn_subassets.clicked.connect(partial(self.appFunction.btnToolClicked, "ExportSubasset"))
        self.view.publishBtn.clicked.connect(partial(self.appFunction.btnExportClicked, "Publish"))
        self.view.publishSubassetBtn.clicked.connect(partial(self.appFunction.btnExportClicked, "PublishSubasset"))
        # self.view.history_list.doubleClicked.connect(self.appFunction.change_version)

    def createAsset(self, control):
        self._utils.control = control
        self._utils.createAsset()

    def get_env(self):

        module_path = os.__file__
        if "Engine\\Binaries\\ThirdParty" in module_path:
            return "Unreal"
        if "Maya" in module_path:
            return "Maya"
        if "HOUDIN" in module_path:
            return "Houdini"
        if global_setting.DEBUG:
            return "Unreal"
        return None