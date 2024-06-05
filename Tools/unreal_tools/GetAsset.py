#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2022/12/2 0:04
"""
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(600, 400)
        self.label = QtWidgets.QLabel("选择路径")
        self.pathLine = QtWidgets.QLineEdit()
        self.browser = QtWidgets.QPushButton("Browser")
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["assetName", "LODBias", "nameRule", "resolutionRule", "isPower"])
        self.check = QtWidgets.QPushButton("Check")

        self.lay1 = QtWidgets.QHBoxLayout()
        self.lay1.addWidget(self.label)
        self.lay1.addWidget(self.pathLine)
        self.lay1.addWidget(self.browser)

        self.lay2 = QtWidgets.QVBoxLayout()
        self.lay2.addLayout(self.lay1)
        self.lay2.addWidget(self.table)
        self.lay2.addWidget(self.check)
        self.setLayout(self.lay2)




if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    import re
    import os
    import json
    import sys
    # import unreal
    import subprocess


    def CheckTextureNameRule(checkType, assetName):
        if checkType == 'Texture2D':
            if not assetName.startswith('T_'):
                return False
        if checkType == 'StaticMesh':
            if not assetName.startswith('SM_'):
                return False
        return True


    def isPower(sizeX, sizeY):
        if sizeX < 1 or sizeY < 1:
            return False
        m = sizeX & (sizeX - 1)
        n = sizeY & (sizeY - 1)
        return m == 0 or n == 0


    def lodBias(num):
        if num != 0:
            return False
        return True


    def CheckTextureResolution(sizeX, sizeY):
        if sizeX and isinstance(sizeX, str):
            sizeX = int(sizeX)
        if sizeY and isinstance(sizeY, str):
            sizeY = int(sizeY)
        maxSize = max(sizeX, sizeY)
        if maxSize > 4096:
            return False
        return True


    def CheckTextureCompressionSetting(assetName, CompressionSetting):
        if assetName.endswith('ORM') or assetName.endswith('ORH') or assetName.endswith('OGS') or assetName.endswith(
                'Mask') or assetName.endswith('_M'):
            if 'TC_MASKS' not in CompressionSetting:
                return False
        return True


    def findErrorFile(changeListNumber):
        checkOutput = {}
        if changeListNumber == 1:
            changeListNumber = 'head'
        cmd = 'p4 files @={changeListNumber}'.format(changeListNumber=changeListNumber)
        p4Process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        res_files, err = p4Process.communicate()
        for res in res_files.decode('utf-8', 'ignore').split('\\r\\n'):
            if not res or 'delete' in res:
                continue
            res = re.sub(r'#\d.*[)]', '', res).split('/Content/')[-1]
            unrealPath = ('/Game/' + res).replace('uasset', res.split('/')[-1].split('.')[0])
            if res.startswith('/Game/UI') or res.startswith('/Game/VX'):
                continue
            assetData = unreal.EditorAssetLibrary.find_asset_data(unrealPath)
            if assetData.asset_class == 'Texture2D':
                packageName = assetData.package_name
                assetName = assetData.asset_name
                checkOutput[str(packageName)] = {}
                CompressionSetting = assetData.get_asset().get_editor_property('compressionsettings')
                sizeX = assetData.get_asset().blueprint_get_size_x()
                sizeY = assetData.get_asset().blueprint_get_size_y()
                LODBias = assetData.get_asset().lod_bias
                checkOutput['validate'] = True
                if not CheckTextureNameRule('Texture2D', str(assetName)):
                    checkOutput['validate'] = False
                if not CheckTextureResolution(sizeX, sizeY):
                    checkOutput['validate'] = False
                if not isPower(sizeX, sizeY):
                    checkOutput['validate'] = False
                if not lodBias(LODBias):
                    checkOutput['validate'] = False
                checkOutput[str(packageName)].update({'LODBias': lodBias(LODBias)})
                checkOutput[str(packageName)].update({'nameRule': CheckTextureNameRule('Texture2D', str(assetName))})
                checkOutput[str(packageName)].update({'resolutionRule': CheckTextureResolution(sizeX, sizeY)})
                checkOutput[str(packageName)].update({'isPower': isPower(sizeX, sizeY)})
                checkOutput[str(packageName)].update(
                    {'Compression_setting': CheckTextureCompressionSetting(str(assetName), CompressionSetting)})
            if assetData.asset_class == 'StaticMesh':
                packageName = assetData.package_name
                assetName = assetData.asset_name
                checkOutput[str(packageName)] = {}
                NumLods = assetData.get_asset().get_num_lods()
                if NumLods > 4:
                    checkOutput['validate'] = False
                    checkOutput[str(packageName)].update({'NumLods': False})