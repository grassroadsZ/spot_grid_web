# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 10:54
# @Author  : grassroadsZ
# @File    : Ding_Ding.py
import json
from datetime import datetime

import requests

dingding_token = ""


def send_dingding_msg(content):
    """
    :param content:
    :param robot_id:  你的access_token，即webhook地址中那段access_token。例如如下地址：https://oapi.dingtalk.com/robot/
n    :param secret: 你的secret，即安全设置加签当中的那个密钥
    :return:
    """
    try:
        msg = {
            "msgtype": "text",
            "text": {"content": datetime.now().strftime("%m-%d %H:%M:%S") + "\n"+content + '\n' }}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        # https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX

        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + dingding_token
        body = json.dumps(msg)
        requests.post(url, data=body, headers=headers, timeout=10)
    except Exception as e:
        print("发送钉钉失败:", e)


if __name__ == '__main__':
    send_dingding_msg("通知:测试一下")
