# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'commentView.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from AssetBrowser.view.baseWidget import QComboCheckBox


class CommentUI(QWidget):

    def __init__(self, parent=None):
        super(CommentUI, self).__init__(parent)
        self._members = None
        self.setupUi()

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        self._members = value

    def setupUi(self):

        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(self.frame)
        self.radioButton.setChecked(True)
        self.radioButton.setText(u"通知人员")
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout.addWidget(self.radioButton)

        self.comboBox = QComboCheckBox()

        # self.comboBox.add_items(["秦家鑫", '王若男', '王元昊', '刘雅旭'])
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame)
        self.label.setText("任务ID")
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalLayout_2.addWidget(self.frame)


if __name__ == '__main__':
    import sys
    import os
    import json
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.ico')))
    noticeConfig = os.path.join(os.path.dirname(__file__), 'noticeConfig.json')
    with open(noticeConfig, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    window = CommentUI()
    window.comboBox.add_items(data.keys())
    window.comboBox.select_clear()
    window.show()
    app.exec_()
