# _*_coding:utf-8 _*_
from functools import partial
from PySide2 import QtWidgets, QtCore
from AssetBrowser.modules.global_setting import STEP


class StepWidget(QtWidgets.QDialog):
    def __init__(self, current_step, parent=None):
        super(StepWidget, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.select_step = None
        self.setStyleSheet('''
        
        QDialog {
        background-color: #36393f;
        }
        QLabel {
        font: 10pt "Consolas";
        color: rgb(202, 202, 202);
        }
        QPushButton{
                    font: 15pt "Consolas";
                    color: rgb(202, 202, 202);
                    border-radius: 20px;
                    background-color: #5285a6;
                    background-repeat: no-repeat;
                    background-position: left center;
                }
        QPushButton:hover { background-color: #0a82c8; border-style: solid; border-radius: 20px; }
        QPushButton:pressed { background-color: #0a82c8; border-style: solid; border-radius: 20px; }

        
        QComboBox {
                font: 10pt "Consolas";
                color: rgb(202, 202, 202);
                border: 1px solid rgb(117, 118, 118);
                border-radius: 5px;
                background: #36393f;
                padding: 1px 2px 1px 2px;
                
                }
        QComboBox QAbstractItemView {
            outline: 0px solid gray;
            border: #36393f;
            color: rgb(202, 202, 202);
            background-color: #36393f;
            selection-background-color: #5285a6;
        }

        ''')
        self.setWindowTitle(u"选择")
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        current_label = QtWidgets.QLabel(u"确认环节为：{0}".format(current_step))
        current_label.setStyleSheet("font-size: 24pt")

        self.layout.addWidget(current_label)
        btn_layout = QtWidgets.QHBoxLayout()
        self.step_combo = QtWidgets.QComboBox()
        self.step_combo.addItems(STEP)

        index = self.step_combo.findText(current_step, QtCore.Qt.MatchFixedString)
        self.step_combo.setCurrentIndex(index)
        btn_layout.addWidget(QtWidgets.QLabel(u"改为："))
        btn_layout.addWidget(self.step_combo)

        self.layout.addLayout(btn_layout)
        self.confirm_btn = QtWidgets.QPushButton(u"确认")
        self.confirm_btn.setMinimumHeight(80)
        self.layout.addWidget(self.confirm_btn)
        self.confirm_btn.clicked.connect(self.cliecked_close)
        self.setLayout(self.layout)

        self.step_combo.currentIndexChanged.connect(self.set_step)

    def set_step(self):
        self.select_step = self.step_combo.currentText()

    def cliecked_close(self):

        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = StepWidget("Rig")
    window.show()
    app.exec_()