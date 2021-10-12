# _*_coding:utf-8 _*_
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
        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_files, err = process.communicate()
        print(res_files)
        # print(str(res_files, encoding="utf-8"))
        dirs_set = set()
        print(type(res_files.decode('utf-8')))
        for res in res_files.decode('windows-1252').split('\r\n'):
            print(res)
            if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
                continue
            dirs = res.split(rootPath)[-1].split('/')[0]
            if not re.findall(r'#\d+(.*?)[)]', dirs):
                dirs_set.add(dirs)
        return dirs_set

    def getRegx(self, crType):
        config = self.getConfig()
        if config.get(crType, ''):
            regx = str()
            for cf in config.get(crType).keys():
                if regx:
                    regx = regx + '|{}/(.*?)/'.format(crType) + cf
                else:
                    regx = regx + '{}/(.*?)/'.format(crType) + cf
            return regx
        return None

    def listSubAssetsDir(self, rootPath, crType):
        rootPath = rootPath.replace('\\', '/') + '/'
        cmd_files = 'p4 files ' + rootPath + '...'
        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_files, err = process.communicate()
        dirs_set = set()
        regx = self.getRegx(crType)
        for res in res_files.decode('windows-1252').split('\r\n'):
            if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
                continue
            if not regx:
                continue
            assets = re.findall(regx, res)
            if assets:
                for asset in assets[0]:
                    if asset:
                        dirs_set.add(asset)
        return dirs_set


if __name__ == '__main__':
    _utils = Utils()
    value = _utils.getConfig()
    # print(value)
    from pprint import pprint
    # pprint(value)
    dir_set = _utils.listdir('//Assets/main/TATest')
    for i in dir_set:
        print(i)













