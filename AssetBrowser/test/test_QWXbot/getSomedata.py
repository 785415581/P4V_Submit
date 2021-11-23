#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/17 15:50
"""

import requests
from pprint import pprint
r = requests.get('https://api.github.com/events')
print(r.encoding)
pprint(r.text)
