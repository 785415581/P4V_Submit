# -*- coding: utf-8 -*-
import json
import os
import imp
import importlib


def start_tool(tool_model, **kwargs):
    result = False
    config_dict = read_config()
    soft_env = get_env()

    if not soft_env:
        soft_env = "Default"
    if soft_env not in config_dict:
        log = "Error: Lack {0} import".format(soft_env)
        return log, result

    if tool_model not in config_dict[soft_env]:
        log = "Error: Can't {0} asset in {1}".format(tool_model, soft_env)
        return log, result

    tool_func = config_dict[soft_env][tool_model]["default"]
    # if config_dict[soft_env][tool_model]["ext"][ext]:
    #     tool_func = config_dict[soft_env][tool_model]["ext"][ext]
    if not tool_func:
        log = "Error: no model! "
        return log, False

    module_path = ".".join(tool_func.split(".")[:-1])

    tool_module = importlib.import_module("AssetBrowser.modules.ToolFunction." + module_path)
    imp.reload(tool_module)

    run_func = getattr(tool_module, tool_func.split(".")[-1])
    log, result = run_func(**kwargs)

    return log, result


def read_config():
    config_json = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_json, "r") as f:
        new_dict = json.load(f)
        f.close()
    return new_dict


def get_env():
    module_path = os.__file__
    if "Engine/Binaries/ThirdParty" in module_path:
        return "Unreal"
    if "Maya" in module_path:
        return "Maya"
    if "HOUDIN" in module_path:
        return "Houdini"

    return None


if __name__ == '__main__':
    print(os.__file__)
    new_dict = read_config()
    print(new_dict)
    # from AssetBrowser.modules.ImportFunction import unrealFunctions
    # import AssetBrowser.modules.ImportFunction as ImportFunction
    # run_func = getattr(ImportFunction, "unrealFunctions.UnrealImport")
    # print(run_func)
    tool_model = 'Unreal'
    select_file = 'aaaaa.fbx'
    start_import(tool_model, select_file, type="Character", asset="aaa", step="Rig")