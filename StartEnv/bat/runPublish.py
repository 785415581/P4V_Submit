import sys
import imp
from PySide2 import QtWidgets
sys.path.append("R:/ProjectX/Art/ArtistPersonal/chenghuanhuan/publish")
import AssetBrowser.main as main

        
imp.reload(main)
app = QtWidgets.QApplication(sys.argv)
win = main.MainWindow()
win.show()
app.exec_()