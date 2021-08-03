import os
import yaml


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
            print(config)


if __name__ == '__main__':
    _utils = Utils()
    _utils.getConfig()
