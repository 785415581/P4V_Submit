from PySide2 import QtCore
from Python.modules.app_functions import AppFunction
from Python.modules.p4_module import P4Module
from Python.utils.utils import Utils


class Controller(QtCore.QObject):
    def __init__(self, widget):
        super(Controller, self).__init__()
        self._appFunction = AppFunction(widget)
        self._p4Model = P4Module()
        self._view = widget
        self._utils = Utils()

    def init(self):
        self._p4Model.serverPort = self._view.serverLn.currentText()
        self._p4Model.user = self._view.userLn.currentText()
        self._p4Model.client = self._view.workLn.currentText()

    def initSignal(self):
        self._view.workTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._view.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._view.workTree.customContextMenuRequested.connect(self.appFunction.showWorkTreeHandle)
        self._view.listWidget.customContextMenuRequested.connect(self.appFunction.showWorkListHandle)
        self._view.typeComboBox.currentIndexChanged.connect(self.appFunction.changeType)
        self._view.assetNameComboBox.currentIndexChanged.connect(self.appFunction.changeAsset)
        self._view.submitStepCom.currentIndexChanged.connect(self.appFunction.changeStep)

    def initUI(self):
        self._view.assetNameComboBox.setEnabled(True)
        self._view.typeComboBox.setEnabled(True)
        self._view.currentPathCombox.clear()
        self._view.workTree.clear()
        self._view.listWidget.clear()

    def createAsset(self, control):
        self._utils.control = control
        self._utils.createAsset()

    @property
    def p4Model(self):
        return self._p4Model

    @property
    def appFunction(self):
        return self._appFunction

    @property
    def view(self):
        return self._view
