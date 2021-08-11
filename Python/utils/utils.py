import os
import re
import yaml
import subprocess


class Utils:
    def __init__(self):
        self._control = None

    @property
    def control(self):
        return self._control

    @control.setter
    def control(self, value):
        self._control = value

    def createAsset(self):
        clientRoot = self.control.appFunction.clientRoot
        assetType = self.control.appFunction.typeComboBoxText
        assetName = self.control.appFunction.assetNameComboBoxText
        assetPath = os.path.join(clientRoot, assetType, assetName)
        if not os.path.isdir(assetPath):
            os.mkdir(assetPath)
        with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as fp:
            config = yaml.load(fp.read(), Loader=yaml.FullLoader)
            childFolder = config[assetType]
            if childFolder:
                for folder in childFolder:
                    folderPath = os.path.join(assetPath, folder)
                    os.mkdir(folderPath)

    def formatName(self, filePath):
        aType = self.control.appFunction.typeComboBoxText
        aAsset = self.control.appFunction.assetNameComboBoxText
        aStep = self.control.appFunction.submitStepComText
        print(aType, aAsset, aStep)

    def getConfig(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as fp:
            config = yaml.load(fp.read(), Loader=yaml.FullLoader)
            return config

    @staticmethod
    def listdir(rootPath):
        rootPath = rootPath.replace('\\', '/') + '/'
        cmd_files = 'p4 files ' + rootPath + '...'
        res_files = subprocess.getoutput(cmd_files)
        dirs_set = set()
        for res in res_files.split('\n'):
            dirs = res.split(rootPath)[-1].split('/')[0]
            if not re.findall(r'#\d+(.*?)[)]', dirs):
                dirs_set.add(dirs)
        return dirs_set


if __name__ == '__main__':
    _utils = Utils()
    # value = _utils.getConfig()
    dir_set = _utils.listdir('//Assets/main/Assets')
    print(dir_set)

    # print(value)


    # def execfile(filepath, globals=None, locals=None):
    #     if globals is None:
    #         globals = {}
    #     globals.update({
    #         "__file__": filepath,
    #         "__name__": "__main__",
    #     })
    #     with open(filepath, 'rb') as file:
    #         exec(compile(file.read(), filepath, 'exec'), globals, locals)
    #
    #
    #
    # # Instead of execfile(fn) use exec(open(fn).read()).
    # # https://docs.python.org/3.3/whatsnew/3.0.html?highlight=execfile#builtins
    # # https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
    #
    # # fn = "C:/Users/jiaxin.qin/Desktop/123.py"
    # # exec(compile(open(fn).read(), fn, 'exec'), {"__name__": "__main__"})
    # # exec(open(fn).read())












