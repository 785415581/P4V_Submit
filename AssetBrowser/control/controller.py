from PySide2 import QtCore, QtGui,QtWidgets
from AssetBrowser.modules.app_functions import AppFunction
from P4Module.p4_module import P4Client
from functools import partial

from AssetBrowser.utils.utils import Utils

class AlignDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

class Controller(QtCore.QObject):
    def __init__(self):
        super(Controller, self).__init__()
        self._view = None
        self._utils = Utils()
        self._p4Model = P4Client()
        self._appFunction = AppFunction()
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

        self.view.workTree.clear()
        self.view.workTree.setColumnCount(3)
        self.view.workTree.setHeaderLabels(["Files", "ServerVersion", "LocalVersion"])

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
        self.view.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.assets_file_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.passwordBtn.pressed.connect(self.appFunction.showPassword)
        self.view.passwordBtn.released.connect(self.appFunction.hidePassword)
        self.view.listWidget.customContextMenuRequested.connect(self.appFunction.showWorkTreeHandle)
        self.view.workTree.itemClicked.connect(self.appFunction.listPath)
        self.view.listWidget.itemClicked.connect(self.appFunction.printTest)
        self.view.assets_file_list.customContextMenuRequested.connect(self.appFunction.showWorkListHandle)
        self.view.typeComboBox.currentTextChanged.connect(self.appFunction.changeType)
        self.view.assetNameComboBox.currentTextChanged.connect(self.appFunction.changeAsset)
        self.view.submitStepCom.currentIndexChanged.connect(self.appFunction.changeStep)
        self.view.extend.stateChanged.connect(self.appFunction.extendTree)
        self.view.show_log_check.stateChanged.connect(self.appFunction.show_log)

        self.view.import_select_button.pressed.connect(partial(self.appFunction.Import_btn_clicked, "import"))
        self.view.reference_select_button.pressed.connect(partial(self.appFunction.Import_btn_clicked, "reference"))
        self.view.open_select_button.pressed.connect(partial(self.appFunction.Import_btn_clicked, "open"))
        self.view.down_asset_button.pressed.connect(partial(self.appFunction.Import_btn_clicked, "downAsset"))
        self.view.exportBtn.clicked.connect(partial(self.appFunction.Export_btn_clicked, "ExportScene"))
        self.view.publishBtn.clicked.connect(partial(self.appFunction.Export_btn_clicked, "Publish"))

    def createAsset(self, control):
        self._utils.control = control
        self._utils.createAsset()