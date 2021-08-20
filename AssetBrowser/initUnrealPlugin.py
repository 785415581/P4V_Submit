# -*- coding: utf-8 -*-
import os
import sys
import unreal


def build_env():
    PySide2Lib = r'C:/Python37/Lib/site-packages'
    current_dir = os.path.dirname(os.path.dirname(__file__))
    package_list = [PySide2Lib, current_dir]
    for package in package_list:
        if package not in sys.path:
            sys.path.append(package)


def init():
    menus = unreal.ToolMenus.get()
    menu_name = "LevelEditor.LevelEditorToolBar"
    # if menus.is_menu_registered(menu_name):
    #     menus.remove_menu(menu_name)
    menu = menus.find_menu(menu_name)
    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(u"Asset Browser")
    # entry.set_icon("EditorStyle", "ContentBrowser.AssetActions.Edit")
    typ = unreal.ToolMenuStringCommandType.PYTHON
    entry.set_string_command(typ, "", 'from importlib import reload\nfrom AssetBrowser import main\nreload(main)\nmain.MainWindow().show()')
    menu.add_menu_entry('File', entry)
    menus.refresh_all_widgets()

build_env()
init()