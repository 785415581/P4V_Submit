import os
import yaml


def createAsset(control):
    clientRoot = control.appFunction.clientRoot
    assetType = control.appFunction.typeComboBoxText
    assetName = control.appFunction.assetNameComboBoxText
    assetPath = os.path.join(clientRoot, assetType, assetName)
    if not os.path.isdir(assetPath):
        os.mkdir(assetPath)
    with open('config.yml', 'r') as fp:
        config = yaml.load(fp.read(), Loader=yaml.FullLoader)
        childFolder = config[assetType]
        if childFolder:
            for folder in childFolder:
                folderPath = os.path.join(assetPath, folder)
                os.mkdir(folderPath)


def formatName(control, filePath):
    aType = control.appFunction.typeComboBoxText
    aAsset = control.appFunction.assetNameComboBoxText
    aStep = control.appFunction.submitStepComText

    print(aType, aAsset, aStep)
