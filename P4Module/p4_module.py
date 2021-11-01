# -*- coding: utf-8 -*-
import os
import subprocess
import re

class P4Client(object):
    def __init__(self):
        self._serverPort = "10.0.201.12:1666"

        self.client = None
        self.password = None
        self.clientRoot = None

        p = subprocess.Popen(r"p4 -Ztag -F %User% user -o", stdout=subprocess.PIPE, shell=True)
        outlines = p.stdout.readlines()
        if outlines:
            out = outlines[-1].strip()
            self._user = str(out.decode("utf-8", "ignore"))

    @property
    def serverPort(self):
        return self._serverPort

    @serverPort.setter
    def serverPort(self, value):
        self._serverPort = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def clientRoot(self):
        return self._clientRoot

    @clientRoot.setter
    def clientRoot(self, value):
        self._clientRoot = value

    def validation(self):
        if not self.serverPort:
            return False
        else:
            print('p4 set P4PORT')
            os.popen('p4 set P4PORT={}'.format(self.serverPort))
        if not self.user:
            return False
        else:
            print('p4 set P4USER')
            os.popen('p4 set P4USER={}'.format(self.user))
        if not self.password:
            return False
        else:
            print('p4 set P4PASSWD')
            os.popen('p4 set P4PASSWD={}'.format(self.password))


    @staticmethod
    def getStreamName():
        cmd = 'p4 -F %Stream% -ztag client -o'
        stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if stdout:
            return stdout.decode('windows-1252').split('\r\n')[0]
        return None

    @staticmethod
    def getRoot():
        """
        get current workspace root path
        :return:
        """
        cmd = 'p4 -F %clientRoot% -ztag info'
        stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        if stdout:
            return stdout.decode('windows-1252').split('\r\n')[0]
        return None


    def initClient(self):
        """
        script create new workspace when it hasn't.
        :return:
        """
        initWorkSpaceScriptPath = r'R:/ProjectX/Tools/bat/AutoWorkspace/AutoWorkspace.bat'
        userName = self.user
        password = self.password
        streamName = self.getStreamName()
        depotName = streamName.split("//")[-1].split("/")[0]
        if streamName:
            cmd = '{script} {user} {password} {stream} {depotName}'.format(script=initWorkSpaceScriptPath,
                                                                           user=userName,
                                                                           password=password,
                                                                           stream=streamName,
                                                                           depotName=depotName)
            os.popen(cmd)
        else:
            return False

    def initAssetsClient(self):
        """
        script create new workspace when it hasn't.
        :return:
        """
        initWorkSpaceScriptPath = r'R:/ProjectX/Tools/bat/AutoWorkspaceAssets/AutoWorkspace.bat'
        userName = self.user
        password = self.password
        cmd = '{script} {user} {password}'.format(script=initWorkSpaceScriptPath, user=userName, password=password)
        print(cmd)
        import subprocess
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out = p.stdout.readlines()[-1].strip()
        self.client = str(out.decode("utf-8"))


    def getClienInfo(self):

        data_keys = ["clientName", "clientRoot", "clientStream", "userName"]
        format_keys = ["%{0}%".format(data_key) for data_key in data_keys]
        filters = ";;".join(format_keys)
        cmd = "p4 -F " + filters + " -ztag info"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        infos, err = process.communicate()
        file_dict ={}
        for res in infos.decode('utf-8', "ignore").split('\r\n'):
            if not res:
                continue
            data_values = res.split(";;")


            for index in range(len(data_keys)):
                file_dict[data_keys[index]] = data_values[index]
            # if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
            #     continue
        return file_dict





    def getFiles(self, rootPath):
        file_dict = {}
        rootPath = rootPath.replace('\\', '/') + '/'
        data_keys = ["depotFile", "clientFile", "headRev", "headChange", "haveRev", "headAction"]
        format_keys = ["%{0}%".format(data_key) for data_key in data_keys]
        filters = ";;".join(format_keys)
        cmd_files = "p4 -F "+filters+" -ztag fstat "+rootPath+"..."
        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        res_files, err = process.communicate()
        # print(res_files)
        dirs_set = set()
        #print(res_files.decode('utf-8'))

        for res in res_files.decode('utf-8', "ignore").split('\r\n'):
            if not res:
                continue
            data_values = res.split(";;")

            file_dict.setdefault(data_values[0], {})
            for index in range(len(data_keys)):
                file_dict[data_values[0]][data_keys[index]] = data_values[index]
            # if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
            #     continue
        return file_dict

    def getVersions(self, full_path):
        version_list = []

        cmd_files = 'p4 filelog -t "{0}"'.format(full_path)

        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        res_files, err = process.communicate()
        for res in res_files.decode('utf-8', "ignore").split('\r\n'):
            p = re.compile(r".+#(\d+) change (\d+) .+ on (.+) by (\S+)@.+ '(.+)'")
            match = p.match(res)
            if match:
                version_list.append(match.groups())

        return version_list

    def getLocalVersion(self, full_path):
        cmd_files = "p4 -F %haveRev% -ztag fstat {0}#have".format(full_path)
        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        version, err = process.communicate()
        if version:
            return version.decode("utf-8", "ignore")
        return None

    def getPath(self, have_path):
        cmd_files = "p4 where " + have_path
        process = subprocess.Popen(cmd_files, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        paths, err = process.communicate()
        if paths:
            paths = paths.decode("utf-8", "ignore")
            p = re.compile(r"(.+) (.+) (.+)")
            match = p.match(paths)
            if match:
                serve_path, workspace_path, local_path = match.groups()
                return serve_path, workspace_path, local_path

        return None, None, None

    def createNewChangelist(self, description="My pending change"):
        #todo test chinese
        cmd = 'p4 --field "Description={0}" change -o | p4 change -i'.format(description)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        create_info, err = process.communicate()

        if err:
            return err, False
        change_re = re.compile(r"Change (\d+) created")
        match = change_re.match(create_info.decode("utf-8", "ignore"))
        if not match:
            return "Error: Failed to create new changelist {0}".format(create_info), False

        return match.groups()[0], True

    def checkout(self, local_files, publish_log="Auto Publish"):
        data_keys = ["depotFile", "clientFile", "headRev", "headChange", "haveRev", "headAction"]
        format_keys = ["%{0}%".format(data_key) for data_key in data_keys]
        filters = ";;".join(format_keys)
        add_key = "%no such file%"

        new_change, res = self.createNewChangelist(publish_log)
        print(new_change, res)
        if not res:
            return new_change, res

        for local_file in local_files:
            cmd_stat = "p4 -F " + filters + " -ztag fstat " + local_file
            process = subprocess.Popen(cmd_stat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            res_files, err = process.communicate()

            for res in res_files.decode('utf-8', "ignore").split('\r\n'):
                if not res:
                    continue
                data_values = res.split(";;")

                if not data_values[0]:
                    add_cmd = "p4 add -d -c {0} {1}".format(new_change, local_file)
                    process = subprocess.Popen(add_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()
                    out=out.decode('utf-8', "ignore")

                    if err:
                        return err, False
                    if "reopen" in out:
                        reopen_cmd = "p4 reopen -c {0} {1}".format(new_change, local_file)
                        process = subprocess.Popen(reopen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        out, err = process.communicate()
                else:
                    edit_cmd = "p4 edit -c {0} {1}".format(new_change, local_file)
                    print(edit_cmd)
                    process = subprocess.Popen(edit_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()
                    out = out.decode("utf-8", "ignore")
                    if "reopen" in out:
                        reopen_cmd = "p4 reopen -c {0} {1}".format(new_change, local_file)
                        process = subprocess.Popen(reopen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        out, err = process.communicate()


                    sync_cmd = "p4 sync {0}".format(local_file)
                    print(sync_cmd)
                    process = subprocess.Popen(sync_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()


                    resolve_cmd = "p4 resolve -ay {0}".format(local_file)
                    print(resolve_cmd)
                    process = subprocess.Popen(resolve_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = process.communicate()

        return new_change, True


    def submitChangelist(self, changeListNum):
        submit_cmd = "p4 submit -c {0}".format(str(changeListNum))
        process = subprocess.Popen(submit_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if err:
            return err, False

        return "Submit success!", True



    def syncFile(self, p4File, version=None):
        cmd = 'p4 sync -f "{}"'.format(p4File)
        if version:
            cmd = 'p4 sync -f "{0}"#{1}'.format(p4File, str(version))
        p = subprocess.Popen(cmd, shell=True)
        return_code = p.wait()

    def syncFiles(self, p4Files):
        for p4File in p4Files:
            pass

    def syncDir(self):
        pass


if __name__ == '__main__':
    p4Module = P4Client()
    p4Module.serverPort = '10.0.201.12:1666'
    p4Module.client = 'qinjiaxin_01YXHY1235_Assets'
    p4Module.user = 'qinjiaxin'
    p4Module.password = 'qinjiaxin_1145qq'
    p4Module.validation()
    root = p4Module.getStreamName()
    print(root)

