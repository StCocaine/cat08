#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : App.py
# @Date  : 2019/2/21
# @User  : tanjun
# @Desc  :
import socket
import logging
import hashlib, base64
import threading
import time
import uuid
from Service import Service
logger = logging.getLogger("debug")
class App:
    @staticmethod
    def run():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 4397;
        sock.bind(('0.0.0.0',4397))
        sock.listen(5)
        cons = {}  # 所有客户端连接存储
        ready = {}  # 对话准备
        logger.debug("启动websock,端口是:" + str(4397))
        while True:
            con, addr = sock.accept()
            key = str(uuid.uuid1()).replace("-","")
            cons[key] = {"con": con, "handshake": False, "name": None}
            service = Service(key, cons, ready)
            service.start()

