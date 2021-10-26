# _*_coding:utf-8 _*_
import os
import re
import sys
sys.path.append("R:\ProjectX\Scripts\Python37\Lib\site-packages")
import yaml
import subprocess
from collections import OrderedDict
import AssetBrowser.modules.global_setting as global_setting
import imp
imp.reload(global_setting)

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
        # if not os.path.isdir(assetPath):
        #     os.mkdir(assetPath)
        # with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as fp:
        #     config = yaml.load(fp.read(), Loader=yaml.FullLoader)
        #     childFolder = config[assetType]
        #     if childFolder:
        #         for folder in childFolder:
        #             folderPath = os.path.join(assetPath, folder)
        #             os.mkdir(folderPath)

    def formatName(self, filePath):
        aType = self.control.appFunction.typeComboBoxText
        aAsset = self.control.appFunction.assetNameComboBoxText
        aStep = self.control.appFunction.submitStepComText
        # print(aType, aAsset, aStep)

    def getConfig(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r') as fp:
            config = yaml.load(fp.read(), Loader=yaml.FullLoader)
            return config

    @staticmethod
    def getPathPre(*argv):
        depot_path_tem = "{0}/Assets/{1}/{2}/{3}".format(*argv)
        return depot_path_tem





    @staticmethod
    def colorText(text, w=False, e=False):

        if w:
            text = "<span style=\" font-size:8pt; font-weight:600; color:#FFA500;\" > {0} </span>".format(text)
        elif e:
            text = "<span style=\" font-size:8pt; font-weight:600; color:#FF0000;\" > {0} </span>".format(text)
        else:
            text = "<span style=\" font-size:8pt; font-weight:600; color:#000000;\" > {0} </span>".format(text)
        return text


    def getAssetsData(self, p4_file_infos):
        data_dicts = OrderedDict()
        half_file_dicts = {}
        full_file_dicts = {}
        asset_type_filter = "|".join(global_setting.ASSETTYPE)
        submit_step_filter = "|".join(global_setting.STEP)

        p = re.compile(r"//Assets/main/Assets/("+ asset_type_filter +")/(.+)/("+ submit_step_filter + ")/(\S+)")
        for p4_file_path, infos in p4_file_infos.items():
            match = p.match(p4_file_path)
            if match:
                asset_type, asset_name, file_type, half_path = match.groups()
                data_key = "{0}_{1}_{2}".format(asset_type, asset_name, file_type)
                data_dicts.setdefault(asset_type, OrderedDict())
                data_dicts[asset_type].setdefault(asset_name, [])
                if file_type not in data_dicts[asset_type][asset_name]:
                    data_dicts[asset_type][asset_name].append(file_type)


                full_file_dicts.setdefault(data_key, []).append(p4_file_path)
                half_file_dicts[p4_file_path] = half_path



        return full_file_dicts, half_file_dicts, data_dicts






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
        for res in res_files.decode('utf-8').split('\r\n'):
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
    from pprint import pprint
    # pprint(value)
    dir_set = _utils.listdir('//Assets/main/TATest')














