# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogAddLabel_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(790, 611)
        Dialog.setStyleSheet(u"background-color: #36393f;")
        self.verticalLayout_4 = QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"\n"
"\n"
"\n"
"QPushButton{\n"
"	font: 10pt \"Consolas\";\n"
"	color: rgb(255, 255, 255);\n"
"    border-radius: 5px;\n"
"    background-color: #5285a6;\n"
"    background-repeat: no-repeat;\n"
"    background-position: left center;\n"
"}\n"
"QPushButton:hover { background-color: #0a82c8; border-style: solid; border-radius: 5px; }\n"
"QPushButton:pressed { background-color: #0a82c8; border-style: solid; border-radius: 5px; }\n"
"\n"
"QListWidget {\n"
"	font: 10pt \"Consolas\";\n"
"	color: rgb(255, 255, 255);\n"
"    background-color: #36393f;\n"
"}\n"
"\n"
"QColumnView {\n"
"	font: 10pt \"Consolas\";\n"
"	color: rgb(255, 255, 255);\n"
"    background-color: #36393f;\n"
"}\n"
"\n"
"/*sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss*/\n"
"\n"
"QLabel {\n"
"font: 10pt \"Consolas\";\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QGroupBox {\n"
"	font: 10pt \"Consolas\";\n"
"	color: rgb(255, 255, 255);\n"
"    background-color: #36393f;\n"
"	border: 1px solid #1e1e1e;\n"
"}\n"
"\n"
"QSplitter"
                        "::handle:horizontal {\n"
"    background-color: #242424;\n"
"}\n"
"QSplitter::handle:vertical {\n"
"    background-color: #242424;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_4 = QGroupBox(self.frame)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton = QRadioButton(self.groupBox_4)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_5.addWidget(self.radioButton)

        self.lineEdit = QLineEdit(self.groupBox_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(70, 16777215))
        self.lineEdit.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.lineEdit)

        self.getFiles = QPushButton(self.groupBox_4)
        self.getFiles.setObjectName(u"getFiles")
        self.getFiles.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_5.addWidget(self.getFiles)

        self.horizontalSpacer_3 = QSpacerItem(442, 8, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 15, 6, 6)
        self.itemListWidget = QListWidget(self.groupBox_3)
        self.itemListWidget.setObjectName(u"itemListWidget")
        self.itemListWidget.setStyleSheet(u"background: #36393f;\n"
"alternate-background-color: #323232;\n"
"")
        self.itemListWidget.setAlternatingRowColors(True)
        self.itemListWidget.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_2.addWidget(self.itemListWidget)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 15, 6, 6)
        self.splitter = QSplitter(self.groupBox)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.levelColumnView = QColumnView(self.splitter)
        self.levelColumnView.setObjectName(u"levelColumnView")
        self.levelColumnView.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.splitter.addWidget(self.levelColumnView)

        self.horizontalLayout.addWidget(self.splitter)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.okBtn = QPushButton(self.frame)
        self.okBtn.setObjectName(u"okBtn")
        self.okBtn.setEnabled(True)
        self.okBtn.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.okBtn)

        self.cancelBtn = QPushButton(self.frame)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.cancelBtn)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Select Label", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"From P4 Get Files", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"\u6309\u7167ChangeList\u53f7\u5bfc\u5165:", None))
        self.getFiles.setText(QCoreApplication.translate("Dialog", u"Get", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Items", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Level", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Label", None))
        self.okBtn.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.cancelBtn.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

