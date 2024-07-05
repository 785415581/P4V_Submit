# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LODExportManage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(546, 534)
        MainWindow.setStyleSheet(u"/* \u5168\u5c40\u5b57\u4f53\u8bbe\u7f6e\u4e3a Consolas */\n"
"* {\n"
"    font-family: Consolas;\n"
"}\n"
"\n"
"/* \u5168\u5c40\u80cc\u666f\u8272\u8bbe\u7f6e\u4e3a\u6df1\u7070\u8272 */\n"
"QWidget, QFrame {\n"
"    background-color: #2b2b2b;\n"
"    color: #cccccc; /* \u5168\u5c40\u6587\u672c\u989c\u8272\u8bbe\u7f6e\u4e3a\u6d45\u7070\u8272 */\n"
"}\n"
"\n"
"/* QComboBox \u6837\u5f0f */\n"
"QComboBox {\n"
"    border: 1px solid #555555;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #3c3f41;\n"
"    color: #cccccc;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #888888;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #555555;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: #3c3f41;\n"
"}\n"
"\n"
"QComboBox::down-a"
                        "rrow {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: center center;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    image: none;\n"
"    color: #cccccc;\n"
"    font-size: 14px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QComboBox::down-arrow::on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"        QComboBox:disabled {\n"
"            color: #808080; /* \u7981\u7528\u72b6\u6001\u4e0b\u6587\u672c\u989c\u8272 */\n"
"            background-color: #404040; /* \u7981\u7528\u72b6\u6001\u4e0b\u80cc\u666f\u989c\u8272 */\n"
"            border-color: #404040; /* \u7981\u7528\u72b6\u6001\u4e0b\u8fb9\u6846\u989c\u8272 */\n"
"        }\n"
"/* \u4e0b\u62c9\u5217\u8868\u9879\u6837\u5f0f */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #555555;\n"
"    selection-background-color: #007acc;\n"
"    selection-color: #ffffff;\n"
"    background-color: #3c3f41;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    height: 25px;\n"
"    padding: 2px;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
""
                        "QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #4c5052;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: #007acc;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* QTreeWidget \u6837\u5f0f */\n"
"QTreeWidget {\n"
"    border: 1px solid #555555;\n"
"    background-color: #3c3f41;\n"
"    alternate-background-color: #2b2b2b;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
"QTreeWidget::item {\n"
"    height: 25px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTreeWidget::item:selected {\n"
"    background-color: #007acc;\n"
"    color: white;\n"
"}\n"
"\n"
"QTreeWidget::item:hover {\n"
"    background-color: #4c5052;\n"
"}\n"
"\n"
"/* QHeaderView \u6837\u5f0f */\n"
"QHeaderView::section {\n"
"    background-color: #3c3f41;\n"
"    padding: 4px;\n"
"    border: 1px solid #555555;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
"/* QCheckBox \u6837\u5f0f */\n"
"QCheckBox {\n"
"    spacing: 5px;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width"
                        ": 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    content: \"\u2713\";\n"
"    color: #007acc;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    content: \"\u2717\";\n"
"    color: #555555;\n"
"}\n"
"\n"
"/* QPushButton \u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: #3c3f41;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4c5052;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2b2b2b;\n"
"}\n"
"\n"
"/* QLabel \u6837\u5f0f */\n"
"QLabel {\n"
"    color: #cccccc;\n"
"    background-color: #3c3f41;\n"
"    padding: 5px;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    background-color: #4c5052;\n"
"}\n"
"        /* \u81ea\u5b9a\u4e49\u5782\u76f4\u6eda\u52a8\u6761 */\n"
"        QScrollBar:vertical {\n"
"            border: 2px solid #2b2b2b;\n"
"            background: #2b2"
                        "b2b;\n"
"            width: 15px;\n"
"            margin: 20px 0 20px 0;\n"
"        }\n"
"\n"
"        QScrollBar::handle:vertical {\n"
"            background: #007acc;\n"
"            min-height: 20px;\n"
"            border-radius: 7px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:vertical:hover {\n"
"            background: #5f5f5f;\n"
"        }\n"
"\n"
"        QScrollBar::add-line:vertical {\n"
"            background: #2b2b2b;\n"
"            height: 20px;\n"
"            subcontrol-position: bottom;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"\n"
"        QScrollBar::sub-line:vertical {\n"
"            background: #2b2b2b;\n"
"            height: 20px;\n"
"            subcontrol-position: top;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"\n"
"        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"            border: none;\n"
"            width: 1px;\n"
"            height: 1px;\n"
"            background: none;\n"
"        }\n"
"\n"
"       "
                        " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"            background: none;\n"
"        }\n"
"\n"
"        /* \u81ea\u5b9a\u4e49\u6c34\u5e73\u6eda\u52a8\u6761 */\n"
"        QScrollBar:horizontal {\n"
"            border: 2px solid #2b2b2b;\n"
"            background: #2b2b2b;\n"
"            height: 15px;\n"
"            margin: 0 20px 0 20px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:horizontal {\n"
"            background: #007acc;\n"
"            min-width: 20px;\n"
"            border-radius: 7px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:horizontal:hover {\n"
"            background: #5f5f5f;\n"
"        }\n"
"\n"
"        QScrollBar::add-line:horizontal {\n"
"            background: #2b2b2b;\n"
"            width: 20px;\n"
"            subcontrol-position: right;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"\n"
"        QScrollBar::sub-line:horizontal {\n"
"            background: #2b2b2b;\n"
"            width: 20px;\n"
"            subcontrol-posit"
                        "ion: left;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"\n"
"        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
"            border: none;\n"
"            width: 1px;\n"
"            height: 1px;\n"
"            background: none;\n"
"        }\n"
"\n"
"        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"            background: none;\n"
"        }")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter = QSplitter(self.frame_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_3 = QHBoxLayout(self.page_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.treeWidget = QTreeWidget(self.page_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.horizontalLayout_3.addWidget(self.treeWidget)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout = QVBoxLayout(self.page_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.stackedWidget.addWidget(self.page_4)
        self.splitter.addWidget(self.stackedWidget)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.frame)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEnabled(False)

        self.horizontalLayout.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.frame)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.comboBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 292, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_3.addWidget(self.pushButton_3)

        self.splitter.addWidget(self.frame)

        self.verticalLayout_5.addWidget(self.splitter)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_4.addWidget(self.pushButton_2)

        self.verticalLayout_4.setStretch(0, 10)
        self.verticalLayout_4.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_5.setStretch(0, 10)
        self.verticalLayout_5.setStretch(1, 1)

        self.verticalLayout_6.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 546, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mobile", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"HD_PC", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Level", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"LOD_0", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"LOD_1", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"LOD_2", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"LOD_3", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"LOD_4", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("MainWindow", u"LOD_5", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("MainWindow", u"LOD_6", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("MainWindow", u"LOD_7", None))
        self.comboBox_2.setItemText(8, QCoreApplication.translate("MainWindow", u"LOD_8", None))

        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ExportPath", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Export", None))
    # retranslateUi

