# -*- coding: utf-8 -*-
import os


class BasePublish(object):

    def __init__(self):
        self._control = None
        self._changelist = None

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


    def addChangeList(self, ws_file):
        # p4 查询状态，处理

        return self._changelist, True

    def submit(self):
        if not self._changelist:
            return "Error: failed to get changelist", False

        return "Sucess: finish submit changelist,{0}".format(str(self._changelist)), True


