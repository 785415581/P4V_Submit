# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from AssetBrowser import resources_rc
import AssetBrowser.view.baseWidget as baseWidget


import imp
imp.reload(baseWidget)



class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"Microsoft JhengHei UI")
        self.label.setFont(font)

        # self.horizontalLayout.addWidget(self.label)

        # self.serverLn = QComboBox(self.centralwidget)
        # self.serverLn.addItem("")
        # self.serverLn.setObjectName(u"serverLn")
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        # self.serverLn.setFont(font1)
        # self.serverLn.setEditable(True)

        # self.horizontalLayout.addWidget(self.serverLn)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        # self.label_2 = QLabel(self.centralwidget)
        # self.label_2.setObjectName(u"label_2")
        # self.label_2.setFont(font)
        #
        # self.horizontalLayout_2.addWidget(self.label_2)

        # self.workLn = QComboBox(self.centralwidget)
        # self.workLn.addItem("")
        # self.workLn.setObjectName(u"workLn")
        # self.workLn.setFont(font1)
        # self.workLn.setEditable(True)
        #
        # self.horizontalLayout_2.addWidget(self.workLn)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.userLn = QComboBox(self.centralwidget)
        self.userLn.addItem("")
        self.userLn.setObjectName(u"userLn")
        self.userLn.setFont(font1)
        self.userLn.setEditable(True)

        self.horizontalLayout_3.addWidget(self.userLn)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.passwordLn = QLineEdit(self.centralwidget)
        self.passwordLn.setObjectName(u"passwordLn")
        self.passwordLn.setFont(font1)
        self.passwordLn.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_4.addWidget(self.passwordLn)

        self.passwordBtn = QPushButton(self.centralwidget)
        self.passwordBtn.setObjectName(u"passwordBtn")
        self.passwordBtn.setMinimumSize(QSize(12, 0))
        self.passwordBtn.setFont(font1)
        self.passwordBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.passwordBtn.setStyleSheet(u"QPushButton{\n"
"	min-width:10px;\n"
"    background-color: rgba(39, 44, 54, 0);\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/icons/no_display_password.png);\n"
"}")

        self.horizontalLayout_4.addWidget(self.passwordBtn)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_7.addLayout(self.verticalLayout_3)

        self.connectBtn = QPushButton(self.centralwidget)
        self.connectBtn.setObjectName(u"connectBtn")
        self.connectBtn.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectBtn.sizePolicy().hasHeightForWidth())
        self.connectBtn.setSizePolicy(sizePolicy)
        self.connectBtn.setMinimumSize(QSize(160, 70))
        self.connectBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_7.addWidget(self.connectBtn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"border-top: 1px solid #1e1e1e; background-color: #1e1e1e;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_7.addWidget(self.line)

        self.currentPathCombox = QComboBox(self.centralwidget)
        self.currentPathCombox.setObjectName(u"currentPathCombox")
        self.currentPathCombox.setMinimumSize(QSize(500, 0))
        self.currentPathCombox.setFont(font1)
        self.currentPathCombox.setEditable(True)

        self.verticalLayout_7.addWidget(self.currentPathCombox)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setStyleSheet(u"border-top: 1px solid #1e1e1e; background-color: #1e1e1e;")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)

        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(6,15,6,6)
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.typeComboBox = QComboBox(self.groupBox_3)
        self.typeComboBox.setObjectName(u"typeComboBox")
        self.typeComboBox.setEnabled(False)
        self.typeComboBox.setMinimumSize(QSize(150, 0))
        self.typeComboBox.setFont(font1)
        self.typeComboBox.setEditable(True)

        self.horizontalLayout_5.addWidget(self.typeComboBox)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.assetNameComboBox = QComboBox(self.groupBox_3)
        self.assetNameComboBox.setObjectName(u"assetNameComboBox")
        self.assetNameComboBox.setEnabled(False)
        self.assetNameComboBox.setMinimumSize(QSize(150, 0))
        self.assetNameComboBox.setFont(font1)
        self.assetNameComboBox.setEditable(True)
        pcompleter = QCompleter(self.assetNameComboBox.model())
        self.assetNameComboBox.setCompleter(pcompleter)

        self.horizontalLayout_5.addWidget(self.assetNameComboBox)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.submitStepCom = QComboBox(self.groupBox_3)
        self.submitStepCom.setObjectName(u"submitStepCom")
        self.submitStepCom.setMinimumSize(QSize(150, 0))
        self.submitStepCom.setEditable(True)

        self.horizontalLayout_6.addWidget(self.submitStepCom)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)


        self.horizontalSpacer = QSpacerItem(368, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addWidget(self.groupBox_3)

        tool_layout = QHBoxLayout()

        self.open_scene_button = QPushButton(u"Open Private")
        self.open_scene_button.setObjectName('openSceneButton')
        self.new_scene_button = QPushButton(u"New Scene")
        self.new_scene_button.setObjectName('new_scene_button')
        self.save_scene_button = QPushButton(u"Save Scene")
        self.save_scene_button.setObjectName('save_scene_button')
        self.import_subasset_button = QPushButton("Import SubAssets")
        self.import_subasset_button.setObjectName('import_subasset_button')
        tool_layout.addWidget(self.open_scene_button)
        # tool_layout.addWidget(self.new_scene_button)
        tool_layout.addWidget(self.save_scene_button)
        tool_layout.addWidget(self.import_subasset_button)

        self.horizontalLayout_5.addLayout(tool_layout)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setMinimumSize(QSize(100, 0))
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)

        checkBox_layout = QHBoxLayout()
        self.extend = QCheckBox(u"展开")
        self.show_history = QCheckBox(u"显示history")
        checkBox_layout.addWidget(self.extend)
        checkBox_layout.addWidget(self.show_history)


        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.addLayout(checkBox_layout)
        self.verticalLayout.setContentsMargins(6,15,6,6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.workTree = QTreeWidget(self.groupBox)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.workTree.setHeaderItem(__qtreewidgetitem)
        self.workTree.setObjectName(u"workTree")
        self.workTree.setAlternatingRowColors(True)

        p = QPalette()
        p.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
        self.workTree.setPalette(p)


        self.workTree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.workTree)

        self.import_layout = QHBoxLayout()
        self.import_select_button = QPushButton(u"Import")
        self.import_select_button.setObjectName("importSelectButton")
        self.reference_select_button = QPushButton("Reference")
        self.reference_select_button.setObjectName("reference_select_button")

        self.open_select_button = QPushButton("Open")
        self.open_select_button.setObjectName("open_select_button")

        self.down_select_button = QPushButton("Down")
        self.down_select_button.setObjectName("down_select_button")


        self.import_layout.addWidget(self.import_select_button)
        self.import_layout.addWidget(self.reference_select_button)
        self.import_layout.addWidget(self.open_select_button)
        self.import_layout.addWidget(self.down_select_button)

        self.verticalLayout.addLayout(self.import_layout)


        self.splitter.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setContentsMargins(6,15,6,6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        # self.tabWidget.setCursor(QCursor(Qt.PointingHandCursor))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_5 = QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter_2 = QSplitter(self.tab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.groupBox_4 = QGroupBox(self.splitter_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget = baseWidget.TreeWidgetDrop(self.groupBox_4)
        self.listWidget.setObjectName(u"listWidget")
        # self.splitter_2.setStretchFactor()


        self.verticalLayout_2.addWidget(self.listWidget)


        self.splitter_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QGroupBox(self.splitter_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 15, 6, 6)
        self.textEdit = QTextEdit(self.groupBox_5)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_4.addWidget(self.textEdit)

        self.splitter_2.addWidget(self.groupBox_5)

        self.verticalLayout_5.addWidget(self.splitter_2)

        export_layout = QHBoxLayout()
        self.exportBtn = QPushButton(self.tab)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setEnabled(False)
        self.exportBtn.setCursor(QCursor(Qt.ForbiddenCursor))
        export_layout.addWidget(self.exportBtn)
        self.exportBtn_subassets = QPushButton("ExportSubAssets")
        self.exportBtn_subassets.setObjectName(u"exportBtn_exportBtn_subassets")
        self.exportBtn_subassets.setCursor(QCursor(Qt.PointingHandCursor))
        export_layout.addWidget(self.exportBtn_subassets)
        self.verticalLayout_5.addLayout(export_layout)

        publish_layout = QHBoxLayout()
        self.publishBtn = QPushButton(self.tab)
        self.publishBtn.setObjectName(u"publishBtn")
        self.publishBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.publishSubassetBtn = QPushButton("PublishSubAssets")
        self.publishSubassetBtn.setObjectName(u"publishSubassetBtn")
        self.publishSubassetBtn.setCursor(QCursor(Qt.PointingHandCursor))
        publish_layout.addWidget(self.publishBtn)
        publish_layout.addWidget(self.publishSubassetBtn)

        self.verticalLayout_5.addLayout(publish_layout)

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")

##################################################
        verticalLayout_5_assets = QVBoxLayout(self.tab_2)
        verticalLayout_5_assets.setObjectName(u"verticalLayout_5")
        self.assets_file_list = QListWidget()
        file_list_layout = QHBoxLayout()
        file_list_layout.addWidget(self.assets_file_list)
        file_list_grp = QGroupBox("File List")
        file_list_grp.setLayout(file_list_layout)

        self.comment_line = QPlainTextEdit()

        comment_layout = QHBoxLayout()
        comment_layout.addWidget(self.comment_line)
        comment_grp = QGroupBox("Comment")
        comment_grp.setLayout(comment_layout)

        verticalLayout_5_assets.addWidget(file_list_grp)
        verticalLayout_5_assets.addWidget(comment_grp)




        self.exportBtn_assets = QPushButton("exportAssets")
        self.exportBtn_assets.setObjectName(u"exportBtn_assets")
        self.exportBtn_assets.setCursor(QCursor(Qt.PointingHandCursor))
        verticalLayout_5_assets.addWidget(self.exportBtn_assets)



        self.publishBtn_assets = QPushButton("publishAssets")
        self.publishBtn_assets.setObjectName(u"publishBtn_assets")
        self.publishBtn_assets.setCursor(QCursor(Qt.PointingHandCursor))
        verticalLayout_5_assets.addWidget(self.publishBtn_assets)

        self.splitter_2.setStretchFactor(0, 1)

############################################################

        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")

        verticalLayout_tab_3 = QVBoxLayout(self.tab_3)
        verticalLayout_tab_3.setObjectName(u"verticalLayout_tab_3")
        self.history_list = QTableView()
        self.history_list.setObjectName("history_list")
        custom_model = baseWidget.CustomModel()
        custom_model.set_header_data(["Revision", "Changelist", "Date Submitted", "Submitted By", "Description"])
        self.history_list.setModel(custom_model)
        self.history_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.history_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.history_list.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        # self.history_list.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        history_list_layout = QHBoxLayout()
        history_list_layout.addWidget(self.history_list)
        history_list_grp = QGroupBox("History List")
        history_list_grp.setLayout(history_list_layout)



        verticalLayout_tab_3.addWidget(history_list_grp)
        verticalLayout_tab_3.setContentsMargins(6,15,6,6)
        # self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_6.addWidget(self.tabWidget)

        self.splitter.addWidget(self.groupBox_2)

        self.verticalLayout_7.addWidget(self.splitter)


        #########add log lineedit
        # import AssetBrowser.modules.app_utils as app_utils
        # app_utils.ParentView().view = self.centralwidget

        #这里的reload不要删，实现maya里重载单例log,
        import AssetBrowser.view.singleton as singleton
        import imp
        imp.reload(singleton)


        self.log_edit = singleton.logEdit
        log_layout = QVBoxLayout()


        log_layout.addWidget(self.log_edit)
        self.groupBox_log = QGroupBox()
        self.groupBox_log.setLayout(log_layout)
        self.groupBox_log.setObjectName(u"groupBox_log")
        self.groupBox_log.setFont(font1)
        self.groupBox_log.setHidden(False)

        self.show_log_check = QCheckBox("ShowLog")
        self.verticalLayout_7.addWidget(self.show_log_check)

        self.verticalLayout_7.addWidget(self.groupBox_log)
        # self.verticalLayout_7.setStretch(0, 0)
        # self.verticalLayout_7.setStretch(1, 0)
        # self.verticalLayout_7.setStretch(2, 0)
        # self.verticalLayout_7.setStretch(3, 0)
        # self.verticalLayout_7.setStretch(4, 5)
        # self.verticalLayout_7.setStretch(5, 2)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 769, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        self.passwordBtn.pressed.connect(self.passwordLn.selectAll)
        self.passwordBtn.pressed.connect(self.passwordBtn.showMenu)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Publish Window", None))
        # self.label.setText(QCoreApplication.translate("MainWindow", u"Server", None))
        # self.serverLn.setItemText(0, QCoreApplication.translate("MainWindow", u"10.0.201.12:1666", None))

        # self.label_2.setText(QCoreApplication.translate("MainWindow", u"Workspace", None))
        # self.workLn.setItemText(0, QCoreApplication.translate("MainWindow", u"qinjiaxin_01YXHY1235_Assets", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"PerforceUser", None))
        # self.userLn.setItemText(0, QCoreApplication.translate("MainWindow", u"qinjiaxin", None))


        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Password      ", None))
        self.passwordBtn.setText("")
        self.connectBtn.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Asset", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.extend.setChecked(True)
        self.show_log_check.setChecked(True)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"AssetName", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"File List", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Comment", None))
        self.exportBtn.setText(QCoreApplication.translate("MainWindow", u"ExportScene", None))
        self.publishBtn.setText(QCoreApplication.translate("MainWindow", u"Publish", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"当前资产提交", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"多资产提交", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  QCoreApplication.translate("MainWindow", u"History", None))


    # retranslateUi

