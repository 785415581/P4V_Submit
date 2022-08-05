#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2022/2/25 17:57
"""
import sys
import unreal
py_lib = r'R:\ProjectX\Scripts\Python37\Lib\site-packages'
if py_lib not in sys.path:
    sys.path.insert(0, py_lib)
from PySide2 import QtWidgets
from PySide2 import QtCore


class ActorMainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ActorMainWindow, self).__init__(parent)
        self.history = list()
        self.resize(642, 424)
        self.setStyleSheet("""
        QWidget{
        background-color: #151515;
        }
        
        QLabel {
        font: 10pt "Consolas";
        color: rgb(202, 202, 202);
        }
        
        QPushButton{
            font: 15pt "Consolas";
            color: #ffffff;
            border-radius: 3px;
            background-color: #8bc24a;
            background-repeat: no-repeat;
            background-position: left center;
        }
        QPushButton:hover { color: #a9c296; border-style: solid; border-radius: 3px; }
        QPushButton:pressed { color: #8bc24a; border-style: solid; border-radius: 3px; }
        
        QTableWidget{
        color:#DCDCDC;
        background:#242424;
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
        self.tipsLabel = QtWidgets.QLabel()
        self.checkButton = QtWidgets.QPushButton()
        self.resultTableWidget = QtWidgets.QTableWidget()
        self.resultTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.resultTableWidget.setColumnCount(4)
        self.resultTableWidget.setHorizontalHeaderLabels(['Actor Label', 'X:长', 'Y:宽', 'Z:高'])
        self.initUI()
        self.initSignal()
        self.setWidgetDescription()

    def initUI(self):
        self.hLay = QtWidgets.QHBoxLayout()
        self.vLay = QtWidgets.QVBoxLayout()

        self.hLay.addWidget(self.tipsLabel)
        self.hLay.addWidget(self.checkButton)
        self.vLay.addLayout(self.hLay)
        self.vLay.addWidget(self.resultTableWidget)
        self.setLayout(self.vLay)

    def setWidgetDescription(self):
        self.tipsLabel.setText("在场景中选中一个或者多个StaticMesh然后点击查询")
        self.checkButton.setText("Check")

    def initSignal(self):
        self.checkButton.clicked.connect(self.buildTable)

    def buildTable(self):
        selectedActors = unreal.LayersSubsystem().get_selected_actors()
        index = 0
        for actor in selectedActors:
            LinearColor = unreal.LinearColor.RED
            v_center, v_event = unreal.GameplayStatics.get_actor_array_bounds([actor], only_colliding_components=False)
            unreal.SystemLibrary.draw_debug_box(unreal.EditorLevelLibrary.get_editor_world(), v_center, v_event,
                                                LinearColor, duration=10, thickness=5)
            x_distance = v_event.x * 2
            y_distance = v_event.y * 2
            z_distance = v_event.z * 2
            print(x_distance, y_distance, z_distance)
            self.resultTableWidget.insertRow(index)
            self.resultTableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(str(actor.get_actor_label())))
            self.resultTableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(str(x_distance)))
            self.resultTableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(str(y_distance)))
            self.resultTableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(str(z_distance)))
            index += 1


if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    global window
    window = ActorMainWindow()
    window.show()
    # app.exec_()
