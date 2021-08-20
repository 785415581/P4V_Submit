import os, marshal
import sys

cmd = input("Enter a Perforce command (omitting 'p4 -G'): ")

#
# basic dictionary read loop using -G flag
#
list = []
if sys.version_info[1] < 6:
    pipe = os.popen('p4 -G ' + cmd, 'r')  # 'rb' on Windows for binary read
else:  # os.popen is deprecated in AssetBrowser 2.6+
    from subprocess import Popen, PIPE
    # p4 client -o qinjiaxin_01YXHY1235_Assets

    pipe = Popen(["p4", "-G"] + cmd.split(), stdout=PIPE).stdout
try:
    while 1:
        record = marshal.load(pipe)
        list.append(record)
except EOFError:
    pass
pipe.close()

# print list of dictionary records
print(list)
# c = 0
# for dict in list:
#     c = c + 1
#     print("\n--%d--" % c)
#     for key in dict.keys():
#         print("%s: %s" % (key, dict[key]))
