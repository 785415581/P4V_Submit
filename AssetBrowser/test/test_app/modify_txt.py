#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/24 15:14
"""

import re
res = []
with open(r"C:\Users\jiaxin.qin\Desktop\workspace_setting.txt", 'r') as fp:
    line = fp.readline()
    while line:
        regx_line = re.findall(r'//.*', line)
        if regx_line:
            if not re.findall(r'//Assets.*', line):
                line = re.sub(r'//.*', '', line)
        res.append(line)
        line = fp.readline()

with open(r"C:\Users\jiaxin.qin\Desktop\workspace_setting.txt", 'w+') as fp:
    for line in res:
        fp.write(line)
    fp.close()



