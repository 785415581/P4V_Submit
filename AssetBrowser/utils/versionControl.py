# -*- coding: utf-8 -*-
import os
import sys
import json
from PySide2 import QtWidgets


run_application_version = dict()


def get_application_version():
    version_list_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/VersionControl.json')
    with open(version_list_path, 'r') as application_version:
        application_version = json.load(application_version)
    return application_version


def set_application_version():
    global run_application_version
    run_application_version = get_application_version()


def check_application_version(application_name, parent):
    global run_application_version
    application_version = get_application_version()
    if run_application_version.get(application_name) != application_version.get(application_name):
        messageBox = QtWidgets.QMessageBox
        messageBox.setStyleSheet(parent, "QMessageBox {color: 1px solid rgb(166, 180, 196);background-color: #36393f;}\n"
                                         "QPushButton {font: 10pt solid;border-radius: 5px;background-color: #5285a6;background-repeat: no-repeat;background-position: left center;}")
        restart = messageBox.critical(parent, "Error", u"工具有更新, 关闭工具后重新开启", QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        if restart == QtWidgets.QMessageBox.Ok:
            sys.exit(0)