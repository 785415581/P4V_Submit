# -*- coding: utf-8 -*-
import os
import getpass
from AssetBrowser.utils import sendMsgWX
from AssetBrowser.modules.global_setting import DEBUG

class BasePublish(object):

    def __init__(self):
        self._control = None
        self._changelist = None
        self.p4Model = None

    @property
    def utils(self):
        if self.control:
            return self.control.utils


    def checkout(self, ws_files, publish_log="Tool Publish"):
        publish_log = publish_log + ":" + getpass.getuser()
        create_return, res = self.p4Model.checkout(ws_files, publish_log = publish_log)
        if not res:
            return create_return, res

        self._changelist = create_return
        return self._changelist, True

    def submit(self):
        if not self._changelist:
            return "Error: failed to get changelist", False

        log, res = self.p4Model.submitChangelist(self._changelist)

        return "Sucess: finish submit changelist,{0}".format(str(self._changelist)), True

    def notice(self, **kwargs):
        if not DEBUG:
            if kwargs.get('isNotice', ''):
                sendMsgWX.send_msg(**kwargs)
                # sendMsgWX.updateTAPDTaskStatus(**kwargs)