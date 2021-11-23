import sys
from PySide2 import QtCore
from PySide2.QtWidgets import *


class TreeWidget(QTreeWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()

        self.setColumnCount(2)  # 共2列
        self.setHeaderLabels(['Key', 'Value'])
        root = QTreeWidgetItem(self)
        root.setText(0, '姓名')
        root.setText(1, 'XerCis')
        root.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)  # 设为可编辑


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TreeWidget()
    win.show()
    sys.exit(app.exec_())
