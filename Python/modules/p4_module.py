import os
import re
import subprocess


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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, value):
        self._clientRoot = value

    def validation(self):
        if not self.serverPort:
            return False
        else:
            print('p4 set P4PORT')
            os.popen('p4 set P4PORT={}'.format(self.serverPort))
        if not self.user:
            return False
        else:
            print('p4 set P4USER')
            os.popen('p4 set P4USER={}'.format(self.user))
        if not self.password:
            return False
        else:
            print('p4 set P4PASSWD')
            os.popen('p4 set P4PASSWD={}'.format(self.password))
        if not self.client:
            return False
        else:
            print('p4 set P4CLIENT')
            os.popen('p4 set P4CLIENT={}'.format(self.client))

    @staticmethod
    def getStreamName():
        cmd = 'p4 -F %Stream% -ztag client -o'
        stdout = subprocess.getoutput(cmd)
        if stdout:
            return stdout
        return None

    @staticmethod
    def getRoot():
        """
        get current workspace root path
        :return:
        """
        cmd = 'p4 -F %clientRoot% -ztag info'
        stdout = subprocess.getoutput(cmd)
        if stdout:
            return stdout
        return None

    def initClient(self):
        """
        script create new workspace when it hasn't.
        :return:
        """
        initWorkSpaceScriptPath = r'R:/ProjectX/Tools/bat/AutoWorkspace/AutoWorkspace.bat'
        userName = self.user
        password = self.password
        streamName = self.getStreamName()
        depotName = 'Assets'
        if streamName:
            cmd = '{script} {user} {password} {stream} {depotName}'.format(script=initWorkSpaceScriptPath,
                                                                           user=userName,
                                                                           password=password,
                                                                           stream=streamName,
                                                                           depotName=depotName)
            os.popen(cmd)
        else:
            return False

    def syncFile(self, p4File):
        cmd = 'p4 sync -s {}'.format(p4File)
        os.popen(cmd)

    def syncFiles(self, p4Files):
        for p4File in p4Files:
            pass

    def syncDir(self):
        pass

if __name__ == '__main__':
    p4Module = P4Module()
    p4Module.serverPort = '10.0.201.12:1666'
    p4Module.client = 'qinjiaxin_01YXHY1235_Assets'
    p4Module.user = 'qinjiaxin'
    p4Module.password = 'qinjiaxin_1145qq'
    p4Module.validation()
    root = p4Module.getRoot()
    print(root)

