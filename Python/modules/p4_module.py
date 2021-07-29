from P4 import P4, P4Exception, DepotFile


class P4Module(object):
    def __init__(self):
        self.serverPort = ''
        self.user = ''
        self.client = ''
        self.password = ''
        self.clientRoot = ''

    def connectP4(self):
        p4 = P4()
        p4.port = self.serverPort
        p4.user = self.user
        p4.password = self.password
        p4.client = self.client
        p4.connect()
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
    p4Module.client = 'qinjiaxin'
    p4Module.user = 'jiaxin.qin'
    p4Module.password = 'jiaxin.qin'
    p4Module.connectP4()