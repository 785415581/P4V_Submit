# -*- coding: utf-8 -*-
import json
import os
import AssetBrowser.modules.ImportFunction as ImportFunction

def start_import(import_model, select_file, current_step):
    log = ""
    result = False
    config_dict = read_config()
    soft_env = get_env()
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
        log ="Error: Lack ext {0} ".format(ext)
        return log, False

    import_func = config_dict[soft_env][import_model]["default"]
    if config_dict[soft_env][import_model]["ext"][ext]:
        import_func = config_dict[soft_env][import_model]["ext"][ext]

    run_func = getattr(ImportFunction, import_func)
    log, result = run_func(select_file, current_step)

    return log, result







def read_config():
    new_dict={}
    config_json = os.path.join(os.path.basename(__file__), "config.json")
    with open(config_json, "w") as f:
        json.dump(new_dict, f)
    return new_dict

def get_env():
    module_path = os.__file__
    if "Engine\Binaries\ThirdParty" in module_path:
        return "UE"
    if "Maya" in module_path:
        return "Maya"
    if "HOUDIN" in module_path:
        return "Houdini"

    return None