import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=None)

        self.sequoia = Sequoia()
        self.baobab = Baobab()
        self.c_widget = QtWidgets.QWidget()
        h_boxlayout = QtWidgets.QHBoxLayout(self.c_widget)
        self.setCentralWidget(self.c_widget)
        h_boxlayout.addWidget(self.sequoia, 30)
        h_boxlayout.addWidget(self.baobab, 70)


class Sequoia(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(Sequoia, self).__init__(parent=None)
        self.setColumnCount(2)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)

        self.sampleitem = QtWidgets.QTreeWidgetItem()
        self.sampleitem.setText(0,"a")
        self.sampleitem.setText(1,"b")
        self.addTopLevelItem(self.sampleitem)


class Baobab(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(Baobab, self).__init__(parent=None)
        self.setColumnCount(2)
        self.setAcceptDrops(True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    main()