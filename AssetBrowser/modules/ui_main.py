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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(769, 726)
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

        self.horizontalLayout.addWidget(self.label)

        self.serverLn = QComboBox(self.centralwidget)
        self.serverLn.addItem("")
        self.serverLn.setObjectName(u"serverLn")
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        self.serverLn.setFont(font1)
        self.serverLn.setEditable(True)

        self.horizontalLayout.addWidget(self.serverLn)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.workLn = QComboBox(self.centralwidget)
        self.workLn.addItem("")
        self.workLn.setObjectName(u"workLn")
        self.workLn.setFont(font1)
        self.workLn.setEditable(True)

        self.horizontalLayout_2.addWidget(self.workLn)

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
        self.connectBtn.setMinimumSize(QSize(160, 110))
        self.connectBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.connectBtn.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Custom */\n"
"#connectBtn{ font-family: \"Microsoft YaHei\";\n"
"    font-size: 15px;\n"
"	font-color:#2b2b2b;\n"
"border-radius: 20px;\n"
"background-color: #214283;\n"
"background-repeat: no-repeat;\n"
"background-position: left center;\n"
"}\n"
"#connectBtn:hover { background-color: #282c34; border-style: solid; border-radius: 20px; }\n"
"#connectBtn:pressed { background-color: #214283; border-style: solid; border-radius: 20px; }")

        self.horizontalLayout_7.addWidget(self.connectBtn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
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
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
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
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.workTree = QTreeWidget(self.groupBox)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.workTree.setHeaderItem(__qtreewidgetitem)
        self.workTree.setObjectName(u"workTree")
        self.workTree.setStyleSheet(u"QTreeWidget::branch:closed:has-children{\n"
"    image:url(icons/close_folder.png);\n"
"}\n"
"\n"
"QTreeWidget::branch::open::has-children{\n"
"    image:url(icons/open_folder.png);\n"
"}\n"
"")
        self.workTree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.workTree)

        self.splitter.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.listWidget = QListWidget(self.groupBox_4)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)

        self.splitter_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QGroupBox(self.splitter_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QTextEdit(self.groupBox_5)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_4.addWidget(self.textEdit)

        self.splitter_2.addWidget(self.groupBox_5)

        self.verticalLayout_5.addWidget(self.splitter_2)

        self.publishBtn = QPushButton(self.tab)
        self.publishBtn.setObjectName(u"publishBtn")
        self.publishBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_5.addWidget(self.publishBtn)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout = QGridLayout(self.tab_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        font2 = QFont()
        font2.setFamily(u"Consolas")
        font2.setPointSize(16)
        self.label_8.setFont(font2)

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_6.addWidget(self.tabWidget)

        self.splitter.addWidget(self.groupBox_2)

        self.verticalLayout_7.addWidget(self.splitter)

        self.verticalLayout_7.setStretch(5, 5)
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Server", None))
        self.serverLn.setItemText(0, QCoreApplication.translate("MainWindow", u"10.0.201.12:1666", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Workspace", None))
        self.workLn.setItemText(0, QCoreApplication.translate("MainWindow", u"qinjiaxin_01YXHY1235_Assets", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"User", None))
        self.userLn.setItemText(0, QCoreApplication.translate("MainWindow", u"qinjiaxin", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.passwordBtn.setText("")
        self.connectBtn.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Asset", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"AssetName", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"File List", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Comment", None))
        self.publishBtn.setText(QCoreApplication.translate("MainWindow", u"Publish", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u5355\u6587\u4ef6\u63d0\u4ea4", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Under functional development...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u591a\u6587\u4ef6\u63d0\u4ea4", None))
    # retranslateUi

