#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: 785415581@qq.com
Date: 2021/12/10 16:30
"""
import os
import re
import sys
import unreal
import subprocess

try:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
except ImportError:
    pass


class CheckChange(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1010, 690)
        self.setStyleSheet("""
        QWidget{background-color: #242424;}
        QPushButton{
        font-family: \"Microsoft YaHei\";
        font-size: 15px;
        color: #c0c0c0;
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
        QLabel{
        font-family: \"Microsoft YaHei\";
        font-size: 15px;
        color: #c0c0c0;
        background-color: #383838;
        border-radius: 5px;
        }
        QLineEdit{
        font-family: \"Microsoft YaHei\";
        font-size: 15px;
        color: #c0c0c0;
        background-color: #383838;
        border-radius: 5px;
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
        self.sortUpDown = True
        self._file_list = {}
        contentPath = unreal.Paths()
        self.project_dir = contentPath.project_dir()
        self.changeNumberLabel = QtWidgets.QLabel()
        self.lineEdit = QtWidgets.QLineEdit()
        self.checkBtn = QtWidgets.QPushButton()
        self.changePathLabel = QtWidgets.QLabel()
        self.changePathEdit = QtWidgets.QLineEdit()
        self.changePathCheckBtn = QtWidgets.QPushButton()
        self.tableWidget = QtWidgets.QTableWidget()
        self.hlay = QtWidgets.QHBoxLayout()
        self.vlayMain = QtWidgets.QVBoxLayout()

        self.initUI()
        self.layoutWidget()
        self.initSignal()

    def initUI(self):
        self.changeNumberLabel.setText(u'输入change list号：')
        self.checkBtn.setText("Check")
        self.changePathLabel.setText("路径")
        self.changePathCheckBtn.setText("Check")

        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setSortIndicator(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Action', 'Actor Label', 'Actor Path'])

    def initSignal(self):
        self.checkBtn.clicked.connect(self.get_p4_files)
        self.changePathCheckBtn.clicked.connect(self.getActorFromPath)
        self.tableWidget.clicked.connect(self.focusActor)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sortTableByCol)

    def layoutWidget(self):
        self.hlay.addWidget(self.changeNumberLabel)
        self.hlay.addWidget(self.lineEdit)
        self.hlay.addWidget(self.checkBtn)

        self.hlay1 = QtWidgets.QHBoxLayout()
        self.hlay1.addWidget(self.changePathLabel)
        self.hlay1.addWidget(self.changePathEdit)
        self.hlay1.addWidget(self.changePathCheckBtn)

        self.vlayMain.addLayout(self.hlay)
        self.vlayMain.addLayout(self.hlay1)
        self.vlayMain.addWidget(self.tableWidget)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayMain)

    def getActorFromPath(self):
        self._clearTableWidget()
        path = self.changePathEdit.text()
        if 'ProjectX/Content' in path:
            local_suf = path.split('ProjectX/Content')[-1]
        elif "/Content" in path:
            local_suf = path.split('/Content')[-1]
        else:
            local_suf = path
        if local_suf:
            local_suf = "/Game" + local_suf.replace(".uasset", "")
            local_suf = local_suf.replace("\\", '/')
            # actorName, className = unreal.XPTAEToolsBPLibrary.get_actor_name_from_partition_actor_asset_path_name(local_suf)
            # rowCount = self.tableWidget.rowCount()
            # self.tableWidget.insertRow(rowCount)
            # self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(actorName)))
            # self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(local_suf))

    def _clearTableWidget(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            self.tableWidget.removeRow(i)

    def focusActor(self, index):
        command = "CAMERA ALIGN ACTIVEVIEWPORTONLY"
        if index.column() == 0 and index.data() is not None:
            all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
            for actor in all_actors:
                label = actor.get_actor_label()
                if label == index.data():
                    unreal.EditorLevelLibrary.set_selected_level_actors([actor])
                    # unreal.XPTAEToolsBPLibrary.execute_console_command(command)

    def get_p4_files(self):
        self.initP4()
        change_list = self.lineEdit.text()
        streamRoot_cmd = "p4 -F %clientStream% -ztag info"
        process = subprocess.Popen(streamRoot_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        streamRoot, err = process.communicate()
        streamRoot = streamRoot.decode('utf-8', "ignore").split('\r\n')[0]
        cmd = 'p4 files {streamRoot}/ @{changelist},{changelist}'.format(streamRoot=streamRoot, changelist=int(change_list))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        res_files, err = process.communicate()
        for res in res_files.decode('utf-8', "ignore").split('\r\n'):
            if not res or "delete" in res:
                continue
            if ".uasset" in res:
                suf = res.split('.uasset')[0]
                action = res.split('.uasset')[-1]
                action = re.findall(r'#\d+ - (.*) change', action)
                local_suf = suf.split('/Content')
                if local_suf:
                    local_suf = "/Game" + local_suf[-1]
                    self._file_list[local_suf] = (local_suf, action[0])

        self.get_res(self._file_list)

    def get_res(self, res):
        self._clearTableWidget()
        # for key, value in res.items():
        #     actorName, className = unreal.XPTAEToolsBPLibrary.get_actor_name_from_partition_actor_asset_path_name(key)
        #     clientRoot_cmd = "p4 -F %clientRoot% -ztag info"
        #     process = subprocess.Popen(clientRoot_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #     clientRoot, err = process.communicate()
        #     clientRoot = clientRoot.decode('utf-8', "ignore").split('\r\n')[0]
        #     path = clientRoot + value[0].replace('/Game', '/Content') + '.uasset'
        #     rowCount = self.tableWidget.rowCount()
        #     self.tableWidget.insertRow(rowCount)
        #     if key:
        #         self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(actorName)))
        #         self.tableWidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(value[1]))
        #         self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(path))
        #     else:
        #         self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(u"未查询出Actor(或已删除)"))
        #         self.tableWidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(value[1]))
        #         self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(path))

    def sortTableByCol(self, col):
        if self.sortUpDown:
            self.tableWidget.sortItems(col, QtCore.Qt.AscendingOrder)
            self.sortUpDown = False
        else:
            self.tableWidget.sortItems(col, QtCore.Qt.DescendingOrder)
            self.sortUpDown = True

    def initP4(self):
        pass
        # contentP4Info = unreal.XPTAEToolsBPLibrary.get_p4_info()
        # contentP4Info = {
        #     "Server": "10.0.201.12:1666",
        #     "UserName": "qinjiaxin",
        #     "WorkSpace": "qinjiaxin_01YXHY1235_Cyberpunk"
        # }
        # os.popen('p4 set P4PORT={}'.format(contentP4Info.get('Server')))
        # os.popen('p4 set P4USER={}'.format(contentP4Info.get('UserName')))
        # os.popen('p4 set P4CLIENT={}'.format(contentP4Info.get('WorkSpace')))


if __name__ == "__main__":
    import os
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    global window
    window = CheckChange()
    window.show()
    # app.exec_()





