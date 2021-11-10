import os
doc_path = os.path.expanduser("~")+"/Documents"
maya_path = os.path.join(doc_path, "maya")
houdini_path = os.path.join(doc_path, "houdini18.5")

if not os.path.exists(maya_path):
    os.makedirs(maya_path)

if not os.path.exists(houdini_path):
    os.makedirs(houdini_path)

maya_env_file = os.path.join(maya_path, "Maya.env")
houdini_env_file = os.path.join(houdini_path, "houdini.env")


def write_env(env_file, env_name, script_path):
    lines = []
    houdini_flag=False
    if os.path.exists(env_file):
        with open(env_file, "r") as rf:
            for line in rf.readlines():
                if line.startswith(env_name):
                    houdini_flag=True
                    if script_path not in line:
                        line = line.rstrip("\n") + r";{0}\n".format(script_path)
                lines.append(line)

    if not houdini_flag:
        lines.append("{env}=${env};{script}".format(env=env_name, script=script_path))

    with open(env_file, "w") as wf:
        wf.writelines(lines)
        wf.close()

write_env(houdini_env_file,
          "HOUDINI_PATH",
          "R:/ProjectX/Scripts/Python/tools/publish/StartEnv/houdini")
write_env(maya_env_file,
    "MAYA_SCRIPT_PATH",
    "R:/ProjectX/Scripts/Python/tools/publish/StartEnv/maya/scripts")



