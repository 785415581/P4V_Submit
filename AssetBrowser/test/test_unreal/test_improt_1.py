import os    
import sys    
DIR = os.path.dirname(__file__)    
vendor = os.path.join(DIR, "vendor")    
sys.path.insert(0, vendor) if vendor not in sys.path else None    
# NOTE 添加 FBXImporter 路径    
FBX = os.path.join(DIR, "FBXImporter")    
sys.path.insert(0, FBX) if FBX not in sys.path else None    


import unreal    
from Qt import QtWidgets    
from Qt import QtCore    
from Qt import QtGui    


def slate_deco(func):    
    def wrapper(self, single=True, *args, **kwargs):    
        # NOTE 只保留一个当前类窗口    
        if single:    
            for win in QtWidgets.QApplication.topLevelWidgets():    
                if win is self:    
                    continue    
                elif self.__class__.__name__ in str(type(win)):    
                    win.deleteLater()    
                    win.close()    
        # NOTE https://forums.unrealengine.com/unreal-engine/unreal-studio/1526501    
        # NOTE 让窗口嵌入到 unreal 内部    
        unreal.parent_external_window_to_slate(self.winId())    
        return func(self, *args, **kwargs)    
    return wrapper    


# This function will receive the tick from Unreal    
def __QtAppTick__(delta_seconds):    
    QtWidgets.QApplication.processEvents()    
    # NOTE 处理 deleteDeferred 事件    
    QtWidgets.QApplication.sendPostedEvents()    

# This function will be called when the application is closing.    
def __QtAppQuit__():    
    unreal.unregister_slate_post_tick_callback(tick_handle)    


# This part is for the initial setup. Need to run once to spawn the application.    
unreal_app = QtWidgets.QApplication.instance()    
if not unreal_app:    
    unreal_app = QtWidgets.QApplication([])    
    tick_handle = unreal.register_slate_post_tick_callback(__QtAppTick__)    
    unreal_app.aboutToQuit.connect(__QtAppQuit__)    

    # NOTE 重载 show 方法    
    QtWidgets.QWidget.show = slate_deco(QtWidgets.QWidget.show)   
