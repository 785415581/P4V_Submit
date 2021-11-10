import sys
import imp
sys.path.append("R:/ProjectX/Scripts/Python/tools/publish")
from PySide2 import QtWidgets
import AssetBrowser.main as main

        
imp.reload(main)
app = QtWidgets.QApplication(sys.argv)
win = main.MainWindow()
win.show()
app.exec_()