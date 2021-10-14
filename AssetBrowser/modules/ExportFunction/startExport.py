
import json
import os
import AssetBrowser.modules.ExportFunction as ExportFunction
import tempfile
import shutil

def start_export(current_type, current_asset, current_step, export_fold):
    log = ""
    result = False
    config_dict = read_config()
    soft_env = get_env()
    if not soft_env:
        log = u"Error: 没有获取到软件环境"
        return log, result
    if soft_env not in config_dict:
        log = "Error: Lack step {0} under export".format(current_step)

    if current_step not in config_dict[soft_env]:
        log = "Error: Lack {0} export under {1}".format(current_step, soft_env)
        return log, result

    if not config_dict[soft_env][current_step]["files"]:
        log = "Error: Lack export function  under {0}| {1}".format(current_step, soft_env)
        return log, result


    try:
        for file_name, infos in config_dict[soft_env][current_step]["files"].items():
            export_file = os.path.join(export_fold, file_name.replace("XXX", current_asset))

            export_func_name = config_dict[soft_env][current_step]["function"]
            export_func = getattr(ExportFunction, export_func_name)
            export_func(export_file, infos, current_step)
    except Exception as e:

        log = "Error: "+e

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