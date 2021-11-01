
import shutil, os


def moveImportFile(source_path, dst_path):
    copy_to_ws(source_path, dst_path)


def movePublishFile(source_path, dst_path, source_model, have_rev, p4model):
        #todo waiting to deal with file chmod
        if source_model=="server":
            #todo test download seed
            down_to_ws(source_path, dst_path, have_rev, p4model)

        elif source_model=="export":
            copy_to_ws(source_path, dst_path)
            #todo add delete tem file
            # rm_tem_file(source_path)

        elif source_model=="drag":
            copy_to_ws(source_path, dst_path)


def down_to_ws(source_path, dst_path, have_rev, p4model):
    p4model.syncFile(source_path, version=have_rev)
    pass


def copy_to_ws(source_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname(dst_path))
    if os.path.isdir(source_path):
        shutil.copytree(source_path, dst_path)
    else:
        shutil.copyfile(source_path, dst_path)



def rm_tem_file(source_path):
    os.remove(source_path)



