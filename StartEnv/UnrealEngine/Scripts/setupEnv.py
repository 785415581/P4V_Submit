#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/10 16:29
"""
import sys
import unreal


def main():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")

    my_menu = main_menu.add_sub_menu("[My.Menu](http://My.Menu)", "Python", "My Menu", "AuroraTools")

    # for name in ["Open AuroraTools", "Open AuroraTools"]:
    menuEntry = unreal.ToolMenuEntry(
        name="Open AuroraTools",
        type=unreal.MultiBlockType.MENU_ENTRY,
    )
    menuEntry.set_label("Open AuroraTools")
    commandType = unreal.ToolMenuStringCommandType.PYTHON
    menuEntry.set_string_command(commandType, "", 'from StartEnv.UnrealEngine.Scripts import buildEnv\nimport imp\nimp.reload(buildEnv)\nbuildEnv.mainFunc()')
    my_menu.add_menu_entry("Items", menuEntry)



    menuEntry = unreal.ToolMenuEntry(
        name="Tools Box",
        type=unreal.MultiBlockType.MENU_ENTRY,
    )
    menuEntry.set_label("Tools Box")
    commandType = unreal.ToolMenuStringCommandType.PYTHON
    menuEntry.set_string_command(commandType, "",
                                 'from StartEnv.UnrealEngine.Scripts import buildEnv\nimport imp\nimp.reload(buildEnv)\nbuildEnv.Tools()')
    my_menu.add_menu_entry("Items", menuEntry)

    menus.refresh_all_widgets()


if __name__ == '__main__':
    import os

    ToolsLib = r'R:\ProjectX\Scripts\Python\tools\publish'
    site_package = r'R:\ProjectX\Scripts\Python37\Lib\site-packages'
    if os.path.isdir(ToolsLib):
        for libPath in [ToolsLib, site_package]:
            if libPath not in sys.path:
                sys.path.append(libPath)
        main()
