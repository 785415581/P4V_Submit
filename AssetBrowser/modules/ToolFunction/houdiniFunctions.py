
import os
import hou

def houdiniSave(**kwargs):
    file_ext = ".hip"
    import glob
    private_fold = os.path.join(kwargs["localPrePrivate"], "houdini")
    if not os.path.exists(private_fold):
        os.makedirs(private_fold)

    file_pre = "{0}_{1}_v".format(kwargs["asset"].replace("/", "_"), kwargs["step"])
    file_name = file_pre + "*"+ file_ext
    work_file_path = os.path.join(private_fold, file_name)
    version_list = glob.glob(work_file_path)
    if version_list:
        version_list.sort()
        last_version = version_list[-1]
        version_num = os.path.basename(last_version).split(file_ext)[0].split(file_pre)[-1]
        new_version = str(int(version_num)+1).zfill(3)
    else:
        new_version = "001"

    file_name = file_pre + new_version + file_ext
    work_file_path = os.path.join(private_fold, file_name)
    print(1111111111, work_file_path)
    hou.hipFile.save(file_name=work_file_path)

    return "Save File {0}".format(work_file_path), True