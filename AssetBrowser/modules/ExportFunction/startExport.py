
import json
import os
import AssetBrowser.modules.ExportFunction as ExportFunction
import tempfile
import shutil

def start_import(current_step):
    log = ""
    result = False
    config_dict = read_config()
    soft_env = get_env()
    if not soft_env:
        log = u"Error: 没有获取到软件环境"
        return log, result
    if current_step not in config_dict:
        log = "Error: Lack step {0} export".format(current_step)

    if soft_env not in config_dict[current_step]:
        log = "Error: Lack {0} export under {1}".format(soft_env, current_step)
        return log, result

    if not config_dict[current_step][soft_env]:
        log = "Error: Lack export function  under {0}| {1}".format(current_step, soft_env)
        return log, result


    export_func = config_dict[current_step][soft_env]
    export_fold = tempfile.tempdir()
    if not os.path.exists(export_fold):
        os.makedirs(export_fold)

    run_func = getattr(ExportFunction, export_func)
    log, result = run_func(export_fold)

    shutil.rmtree(export_fold)

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