import sys
import imp
sys.path.append("R:/ProjectX/Scripts/Python/tools/publish")
from PySide2 import QtWidgets, QtGui
import AssetBrowser.main as main

        
imp.reload(main)
app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("R:/ProjectX/Scripts/Python/tools/publish/AssetBrowser/icon.ico"))
win = main.FloatingWindow()
win.show()
app.exec_()