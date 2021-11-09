# _*_coding:utf-8 _*_
from functools import partial
from PySide2 import QtWidgets
from AssetBrowser.modules.global_setting import ANIMODEL


class AniModelWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AniModelWidget, self).__init__(parent)
        self.select_model = None
        self.setWindowTitle(u"选择")
        self.layout = QtWidgets.QGridLayout()
        for index in range(len(ANIMODEL)):
            model = ANIMODEL[index]
            btn_dialog01 = QtWidgets.QPushButton(model)
            btn_dialog01.clicked.connect(partial(self.cliecked_close, model))
            self.layout.addWidget(btn_dialog01, 1, index+1)

        self.setLayout(self.layout)

    def cliecked_close(self, model):
        self.select_model = model
        self.close()
