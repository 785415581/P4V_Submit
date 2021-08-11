import os
from P4 import P4, P4Exception, DepotFile


class P4Module(object):
    def __init__(self):
        self._serverPort = None
        self.user = None
        self.client = None
        self.password = None
        self.clientRoot = None

    @property
    def serverPort(self):
        return self._serverPort

    @serverPort.setter
    def serverPort(self, value):
        self._serverPort = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    # @property
    # def password(self):
    #     return self._password
    #
    # @password.setter
    # def password(self, value):
    #     self._password = value

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, value):
        self._clientRoot = value

    def connectP4(self):
        p4 = P4()
        p4.port = self.serverPort
        p4.user = self.user
        # p4.password = self.password
        p4.client = self.client
        p4.connect()
        os.popen(
            r'R:/ProjectX/Tools/bat/AutoWorkspace/AutoWorkspace.bat qinjiaxin qinjiaxin_1145qq //Assets/main Assets')

        connected = p4.connected()
        if connected:
            info = p4.run("info")
            print(info)
            return info
        else:
            return None

    def disconnectP4(self):
        p4 = P4()
        connected = p4.connected()
        if connected:
            p4.disconnect()


if __name__ == '__main__':
    p4Module = P4Module()
    p4Module.serverPort = '10.0.13.18:1666'
    p4Module.client = 'jiaxin.qin_01yxhy1235_projectX'
    p4Module.user = 'jiaxin.qin'
    # p4Module.password = 'jiaxin.qin'
    p4Module.connectP4()