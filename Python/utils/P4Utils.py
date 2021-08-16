import os


def syncFile(p4File):
    cmd = 'p4 sync -f {}'.format(p4File)
    print(cmd)
    os.popen(cmd)


def syncFiles(self, p4Files):
    for p4File in p4Files:
        pass


def syncDir(self):
    pass
