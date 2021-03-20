# -*- coding: utf-8 -*-
# @Time    : 2021/3/17 11:46
# @Author  : grassroadsZ
# @File    : tasks.py
from django import views

from spot_trade.models import SpotConfigModel
from spot_trade.views import help_print, SpotTradeView


class SpotGridViews(views.View):
    def spot_start_run(self):
        help_print("定时任务开始执行")
        try:
            SpotTradeView().loop_run()
        except Exception as e:
            help_print("定时任务异常," + str(e))
