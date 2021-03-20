# -*- coding: utf-8 -*-
# @Time    : 2021/3/17 18:02
# @Author  : grassroadsZ
# @File    : help_func.py
import time


def help_print(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{t}, {msg}", )