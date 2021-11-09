import json
import os
import tempfile


class AppSetting:
    def __init__(self):
        self._fileConfig = os.path.join(tempfile.gettempdir(), 'publish_yxhy.json')

    def init(self):
        default = {'serverPort': [], 'workSpace': [], 'user': [], 'password':[]}
        if not os.path.isfile(self.fileConfig):
            with open(self.fileConfig, 'w', encoding='utf-8') as fp:
                data = json.dumps(default, indent=4)
                fp.write(data)
                fp.close()

    def getConfig(self):

        with open(self.fileConfig, 'r') as fp:
            data = json.loads(fp.read())
            fp.close()

            return data

    def setConfig(self, data):
        with open(self.fileConfig, 'w') as fp:
            data = json.dumps(data)
            fp.write(data)
            fp.close()
            return data

    @property
    def fileConfig(self):
        return self._fileConfig



def add_log(info, error=False, warning=False):

    from AssetBrowser.view.singleton import logEdit
    if warning:
        text = u"<span style=\" font-size:8pt; font-weight:600; color:#FFA500;\" > {0} </span>".format(info)
    elif error:
        text = u"<span style=\" font-size:8pt; font-weight:600; color:#FF0000;\" > {0} </span>".format(info)
    else:
        text = u"<span style=\" font-size:8pt; font-weight:50;\" > {0} </span>".format(info)

    logEdit.appendHtml(text)


class ParentView(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self):
        pass

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        self._view = view




if __name__ == '__main__':
    appSetting = AppSetting()
    appSetting.init()
    # appSetting.getConfig()
