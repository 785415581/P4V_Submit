import os


class BasePublish(object):

    def __init__(self):
        self._appFunction = None
        self._p4Model = None
        self._view = None

    @property
    def appFunction(self):
        return self._appFunction

    @appFunction.setter
    def appFunction(self, func):
        self._appFunction = func

    @property
    def p4Model(self):
        return self._p4Model

    @p4Model.setter
    def p4Model(self, func):
        self._p4Model = func

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, func):
        self._view = func

    def publish(self):
        """Publish files from drag in widget files"""
        print("base publish class")
        print(self.appFunction)
        print(self.p4Model)
        print(self.view)
        pass

    def replaceFile(self):
        """replace local file and submit file to P4"""
        pass
