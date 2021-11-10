import os
os.system(r"net use R: \\10.0.200.5\HeroFileServer")
doc_path = os.path.expanduser("~")+"/Documents"
maya_path = os.path.join(doc_path, "maya")
houdini_path = os.path.join(doc_path, "houdini18.5")

maya_env_file_one = os.path.join(maya_path, "2020", "Maya.env")
maya_env_file_two = os.path.join(maya_path, "2022", "Maya.env")
houdini_env_file = os.path.join(houdini_path, "houdini.env")


def write_env(env_file, env_name, script_path):
    if not os.path.exists(os.path.dirname(env_file)):
        os.makedirs(os.path.dirname(env_file))
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
        lines.append("{env}=${env};{script}\n".format(env=env_name, script=script_path))

    with open(env_file, "w") as wf:
        wf.writelines(lines)
        wf.close()

write_env(houdini_env_file,
          "PYTHONPATH",
          "R:/ProjectX/Scripts/Python/tools/publish")
write_env(maya_env_file_one,
    "PYTHONPATH",
    "R:/ProjectX/Scripts/Python/tools/publish")

write_env(maya_env_file_two,
    "PYTHONPATH",
    "R:/ProjectX/Scripts/Python/tools/publish")


write_env(houdini_env_file,
          "HOUDINI_PATH",
          "R:/ProjectX/Scripts/Python/tools/publish/StartEnv/houdini")
write_env(maya_env_file_one,
    "PYTHONPATH",
    "R:/ProjectX/Scripts/Python/tools/publish/StartEnv/maya/scripts")

write_env(maya_env_file_two,
    "PYTHONPATH",
    "R:/ProjectX/Scripts/Python/tools/publish/StartEnv/maya/scripts")



import win32com.client
import pythoncom


desktop = os.path.expanduser("~") + '/Desktop'
path = os.path.join(desktop, 'runPablish.lnk')
target = r'R:\ProjectX\Scripts\Python\tools\publish\StartEnv\bat\runPublish.bat'
icon = r'R:/ProjectX/Scripts/Python/tools/publish/StartEnv/bat/publish.png'

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.IconLocation = icon
shortcut.WindowStyle = 7
shortcut.save()






