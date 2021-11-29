import sys
import imp
if not sys.path.__contains__("R:/ProjectX/Scripts/Python/tools/publish"):
    sys.path.insert(0, "R:/ProjectX/Scripts/Python/tools/publish")
from PySide2 import QtWidgets, QtGui
import AssetBrowser.main as main

        
imp.reload(main)
app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("R:/ProjectX/Scripts/Python/tools/publish/AssetBrowser/icon.ico"))
win = main.MainWindow()
win.show()
app.exec_()