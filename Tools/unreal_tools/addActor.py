#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/12/28 15:16
"""

import re
import sys
import unreal
import subprocess

SERVER_SITE_PACKAGE = r'R:/ProjectX/Scripts/Python/lib/site-package'

if SERVER_SITE_PACKAGE not in sys.path:
    sys.path.insert(0, SERVER_SITE_PACKAGE)

try:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
except ImportError:
    pass

actor_info = unreal.XPTAEToolsBPLibrary.get_select_partition_actor_asset_name()
p4_info = unreal.XPTAEToolsBPLibrary.get_p4_info()


class AddActor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("""
        QWidget{background-color: #242424;}
        QPushButton{
        font-family: \"Microsoft YaHei\";
        font-size: 15px;
        background-color: #383838;
        border-radius: 5px;
        }
        QPushButton:hover{
        background-color: rgb(180, 141, 238);
        border-style: solid;
        border-radius: 5px;
        }
        QPushButton:pressed {
        background-color: rgb(180, 141, 238);
        border-style: solid;
        border-radius: 4px; 
        }

        /*
        tabelwidget*/
        QTableWidget{
        color:#DCDCDC;
        background:#444444;
        border:1px solid #242424;
        border-radius: 5px;
        alternate-background-color:#525252;/*交错颜色*/
        gridline-color:#242424;
        }

        /*选中item*/
        QTableWidget::item:selected{
        color:#DCDCDC;
        background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);
        }

        /*
        悬浮item*/
        QTableWidget::item:hover{
        background:#5B5B5B;
        }
        /*表头*/
        QHeaderView::section{
        text-align:center;
        background:#5E5E5E;
        padding:3px;
        margin:0px;
        color:#DCDCDC;
        border:1px solid #242424;
        border-left-width:0;
        }
        /*表右侧的滑条*/
        QScrollBar:vertical{
        background:#484848;
        padding:0px;
        border-radius:6px;
        max-width:12px;
        }

        /*滑块*/
        QScrollBar::handle:vertical{
        background:#CCCCCC;
        }
        /*
        滑块悬浮，按下*/
        QScrollBar::handle:hover:vertical,QScrollBar::handle:pressed:vertical{
        background:#A7A7A7;
        }
        /*
        滑块已经划过的区域*/
        QScrollBar::sub-page:vertical{
        background:444444;
        }

        /*
        滑块还没有划过的区域*/
        QScrollBar::add-page:vertical{
        background:5B5B5B;
        }

        /*页面下移的按钮*/
        QScrollBar::add-line:vertical{
        background:none;
        }
        /*页面上移的按钮*/
        QScrollBar::sub-line:vertical{
        background:none;
        }
        """)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))

        self.contentP4Info = dict(p4_info)
        self.contentActorInfo = dict(actor_info)
        contentPath = unreal.Paths()
        self.project_dir = contentPath.project_dir()
        self.syncBtn = QtWidgets.QPushButton()
        self.syncBtn.setText('Sync file')
        self.syncBtn.setPalette(palette)
        self.syncBtn.setEnabled(False)
        self.reconcileBtn = QtWidgets.QPushButton()
        self.reconcileBtn.setText('Reconcile file')
        self.reconcileBtn.setPalette(palette)
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'server version', 'client version', 'path'])
        self.tableWidget.hideColumn(3)
        for key, value in self.contentActorInfo.items():
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(key))
            if value.startswith('/Game'):
                value = value.replace('/Game', 'Content')
                filePath = "{}{}.{}".format(self.project_dir, value, 'uasset')
                headRev, haveRev = self.getReversion(filePath)
                self.tableWidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(headRev))
                self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(haveRev))
                self.tableWidget.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(filePath))
                if headRev != haveRev:
                    self.syncBtn.setEnabled(True)
                    item = self.tableWidget.item(rowCount, 2)
                    item.setBackgroundColor(QtGui.QColor.fromRgb(255, 100, 100))

        self.hlayBtn = QtWidgets.QHBoxLayout()
        self.hlayBtn.addWidget(self.syncBtn)
        self.hlayBtn.addWidget(self.reconcileBtn)
        self.vlayMain = QtWidgets.QVBoxLayout()
        self.vlayMain.addLayout(self.hlayBtn)
        self.vlayMain.addWidget(self.tableWidget)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayMain)
        self.syncBtn.clicked.connect(self.syncFile)
        self.reconcileBtn.clicked.connect(self.reconcileFile)

    def syncFile(self):
        self.initP4()
        rowCount = self.tableWidget.rowCount()
        for i in range(rowCount):
            actorName = self.tableWidget.item(i, 0).text()
            headRev = self.tableWidget.item(i, 1).text()
            haveRev = self.tableWidget.item(i, 2).text()
            filePath = self.tableWidget.item(i, 3).text()
            if headRev != haveRev:
                cmd = 'p4 sync -f %s#head' % filePath
                stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                headRev, haveRev = self.getReversion(filePath)
                self.tableWidget.item(i, 1).setText(headRev)
                self.tableWidget.item(i, 2).setText(haveRev)
                if headRev == haveRev:
                    item = self.tableWidget.item(rowCount, 2)
                    item.setBackgroundColor(QtGui.QColor.fromRgb(220, 220, 220))

    def reconcileFile(self):
        self.initP4()
        rowCount = self.tableWidget.rowCount()
        for i in range(rowCount):
            cmd = 'p4 reconcile -f -m -c default '
            filePath = self.tableWidget.item(i, 3).text()
            if filePath:
                cmd += filePath
            stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            print('reconcile file...')
        QtWidgets.QMessageBox.information(self, 'Tips', 'complete reconcile files',
                                          QtWidgets.QMessageBox.StandardButton.Ok)

    def initP4(self):
        os.popen('p4 set P4PORT={}'.format(self.contentP4Info.get('Server')))
        os.popen('p4 set P4USER={}'.format(self.contentP4Info.get('UserName')))
        os.popen('p4 set P4CLIENT={}'.format(self.contentP4Info.get('WorkSpace')))

    def getReversion(self, filePath):
        self.initP4()
        cmd = 'p4 fstat %s' % filePath
        stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        headRev = None
        haveRev = None
        for i in stdout.decode('windows-1252').split('\r\n'):
            if re.findall('headRev', i):
                headRev = re.findall(r'\w$', i)[0]
            if re.findall('haveRev', i):
                haveRev = re.findall(r'\w$', i)[0]
        return headRev, haveRev


if __name__ == "__main__":
    import os

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    global window
    window = AddActor()
    window.show()
    # app.exec_()
