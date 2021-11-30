# _*_coding:utf-8 _*_

from PySide2 import QtWidgets



class AniModelWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AniModelWidget, self).__init__(parent)
        self.select_model = None
        self.setWindowTitle(u"选择")
        self.layout = QtWidgets.QVBoxLayout()

        lineedit_layout = QtWidgets.QHBoxLayout()

        lineedit_layout.addWidget(QtWidgets.QLabel(u"输入动画模式："))
        self.model_lineedit = QtWidgets.QLineEdit()

        lineedit_layout.addWidget(self.model_lineedit)

        self.layout.addLayout(lineedit_layout)

        self.layout.addWidget(QtWidgets.QLabel("             "))

        self.layout.addWidget(QtWidgets.QLabel(u"格式：[C/S][RF/LF/N]_[Walk/Run/Sprint]_[State]_[F/B/R/L/FL/FR/BL/BR]\n[站蹲姿势][侧身方向]_[武器/道具]_[步调]_[状态]_[移动方向]"))
        self.layout.addWidget(QtWidgets.QLabel("             "))
        btn_dialog01 = QtWidgets.QPushButton(u"确认")
        btn_dialog01.clicked.connect(self.cliecked_close)
        self.layout.addWidget(btn_dialog01)
        self.setLayout(self.layout)

    def cliecked_close(self):
        self.select_model = self.model_lineedit.text()
        self.close()
