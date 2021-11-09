
import os

def defaultNew(**kwargs):

    private_fold = kwargs["localPrePrivate"].replace("/", "\\")
    private_fold = os.path.join(private_fold)
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)
    os.system('explorer {0}'.format(private_fold))
    return "Open Private Fold:{0}".format(private_fold), True



def defaultMayaNew(**kwargs):

    private_fold = kwargs["localPrePrivate"].replace("/", "\\")
    private_fold = os.path.join(private_fold, "maya")
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)
    os.system('explorer {0}'.format(private_fold))
    return "Open Private Fold:{0}".format(private_fold), True

def defaultHoudiniNew(**kwargs):

    private_fold = kwargs["localPrePrivate"].replace("/", "\\")
    private_fold = os.path.join(private_fold, "houdini")
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)
    os.system('explorer {0}'.format(private_fold))
    return "Open Private Fold:{0}".format(private_fold), True


