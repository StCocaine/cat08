#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Main.py
# @Author: Feng
# @Date  : 2019/1/15
# @User  : tanjun
# @Desc  : 启动入口
from Scheduler import Scheduler
import logging.handlers
import os

#logging    初始化工作
logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)
#自动创建文件夹
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):os.mkdir(log_path)
# 添加TimedRotatingFileHandler
# 定义一个1秒换一次log文件的handler
# 保留7个旧log文件
rf_handler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(log_path + "/cat08_spider_debug.log"),when='D',interval=1,backupCount=7)
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

#在控制台打印日志
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(handler)

s = Scheduler();
s.start();