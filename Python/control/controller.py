from PySide2 import QtWidgets
from PySide2 import QtCore
from Python.modules.app_functions import AppFunction
from Python.modules.p4_module import P4Module
from Python.utils.utils import Utils


class Controller(QtCore.QObject):
    def __init__(self):
        super(Controller, self).__init__()
        self._view = None
        self._utils = Utils()
        self._p4Model = P4Module()
        self._appFunction = AppFunction()

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
        self.view.workTree.clear()
        self.view.listWidget.clear()
        self.view.currentPathCombox.clear()
        self.view.typeComboBox.setEnabled(True)
        self.view.assetNameComboBox.setEnabled(True)

    def initUI(self):
        self.p4Model.user = self.view.userLn.currentText()
        self.p4Model.client = self.view.workLn.currentText()
        self.p4Model.serverPort = self.view.serverLn.currentText()

    def initSignal(self):
        self.view.workTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.passwordBtn.pressed.connect(self.appFunction.showPassword)
        self.view.passwordBtn.released.connect(self.appFunction.hidePassword)
        self.view.workTree.customContextMenuRequested.connect(self.appFunction.showWorkTreeHandle)
        self.view.listWidget.customContextMenuRequested.connect(self.appFunction.showWorkListHandle)
        self.view.typeComboBox.currentIndexChanged.connect(self.appFunction.changeType)
        self.view.assetNameComboBox.currentIndexChanged.connect(self.appFunction.changeAsset)
        self.view.submitStepCom.currentIndexChanged.connect(self.appFunction.changeStep)

    def createAsset(self, control):
        self._utils.control = control
        self._utils.createAsset()