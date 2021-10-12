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


if __name__ == '__main__':
    appSetting = AppSetting()
    appSetting.init()
    # appSetting.getConfig()
