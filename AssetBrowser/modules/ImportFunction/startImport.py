# -*- coding: utf-8 -*-
import json
import os
import imp
import importlib
import AssetBrowser.modules.ImportFunction as ImportFunction
DEBUG = False


def start_import(import_model, select_file, **kwargs):
    result = False
    config_dict = read_config()
    soft_env = get_env()
    # TODO: Multi-select import problem
    # for select_file, info in kwargs.items():

    if not soft_env:
        log = u"Error: 没有获取到软件环境"
        return log, result
    if soft_env not in config_dict:
        log = "Error: Lack {0} import".format(soft_env)
        return log, result

    if import_model not in config_dict[soft_env]:
        log = "Error: Can't {0} asset in {1}".format(import_model, soft_env)
        return log, result

    ext = select_file.split(".")[-1]
    if ext not in config_dict[soft_env][import_model]["ext"]:
        log = "Error: Lack ext {0} ".format(ext)
        return log, False

    import_func = config_dict[soft_env][import_model]["default"]
    if config_dict[soft_env][import_model]["ext"][ext]:
        import_func = config_dict[soft_env][import_model]["ext"][ext]
    if not import_func:
        log = "Error: no model! "
        return log, False

    module_path = ".".join(import_func.split(".")[:-1])

    import_module = importlib.import_module("AssetBrowser.modules.ImportFunction." + module_path)
    imp.reload(import_module)

    run_func = getattr(import_module, import_func.split(".")[-1])
    log, result = run_func(select_file, **kwargs)
    return log, result


def read_config():
    config_json = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_json, "r") as f:
        new_dict = json.load(f)
        f.close()
    return new_dict


def get_env():
    module_path = os.__file__
    if "Engine\\Binaries\\ThirdParty" in module_path:
        return "Unreal"
    if "Maya" in module_path:
        return "Maya"
    if "HOUDIN" in module_path:
        return "Houdini"
    if DEBUG:
        return "Unreal"
    return None


if __name__ == '__main__':
    print(os.__file__)
    new_dict = read_config()
    print(new_dict)
    # from AssetBrowser.modules.ImportFunction import unrealFunctions
    # import AssetBrowser.modules.ImportFunction as ImportFunction
    # run_func = getattr(ImportFunction, "unrealFunctions.UnrealImport")
    # print(run_func)
    import_model = 'Unreal'
    select_file = 'aaaaa.fbx'
    start_import(import_model, select_file, type="Character", asset="aaa", step="Rig")