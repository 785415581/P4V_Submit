import os


class BaseExport(object):

    def __init__(self):
        self._control = None

    @property
    def control(self):
        return self._control

    @control.setter
    def control(self, value):
        self._control = value

    @property
    def appFunction(self):
        if self.control:
            return self.control.appFunction

    @property
    def p4Model(self):
        if self.control:
            return self.control.p4Model

    @property
    def view(self):
        if self.control:
            return self.control.view

    @property
    def utils(self):
        if self.control:
            return self.control.utils

    def publish(self):
        """Publish files from drag in widget files"""
        info = self.getSubmitFilesInfo()
        print(info)

    def replaceFile(self):
        """replace local file and submit file to P4"""
        pass

    def getSubmitFilesInfo(self):
        res = dict()
        itemsCount = self.view.listWidget.count()
        for index in range(itemsCount):
            item = self.view.listWidget.item(index)
            res[item.filePath] = {}
            res[item.filePath]['fileName'] = item.fileBaseName.text()
            res[item.filePath]['isChecked'] = item.exportCheck.isChecked()
            res[item.filePath]['submitPath'] = self.view.currentPathCombox.currentText()
            res[item.filePath]['type'] = self.view.typeComboBox.currentText()
            res[item.filePath]['step'] = self.view.submitStepCom.currentText()
            if item.exportCheck.isChecked():
                res[item.filePath]['exportType'] = item.exportType.currentText()
                if hasattr(item.exportPath, 'exportDirectory'):
                    res[item.filePath]['exportPath'] = item.exportPath.exportDirectory
        return res

    def combineConfig(self):
        info = self.getSubmitFilesInfo()
        config = self.utils.getConfig()
