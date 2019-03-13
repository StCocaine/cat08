#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Service.py
# @Date  : 2019/2/21
# @User  : tanjun
# @Desc  : 接收消息,发送消息处理逻辑
from Util import Util
import threading
import copy
import json
import traceback
import logging

logger = logging.getLogger("debug")

class Service(threading.Thread):
    def __init__(self,key,cons={},ready={}):
        # 初始化线程
        threading.Thread.__init__(self)
        self.key = key
        self.ready = ready
        self.cons = cons
        self.conObj = self.cons[self.key]
        self.con = self.conObj["con"]
        self.handshake = self.conObj["handshake"]
        self.init()

    def init(self):
        self.g_code_length = 0;
        self.g_header_length = 0;
        self.buffer_utf8 = b""
        self.length_buffer = 0

    def run(self):
        while True:
            try:
                if self.handshake == False:
                    buffer = self.con.recv(1024)
                    headers = Util.t_header(buffer)
                    try:
                        WebSocketKey = headers["Sec-WebSocket-Key"]
                        if headers["Sec-WebSocket-Protocol"] != "cat08" or headers["Upgrade"] != "websocket" or headers["Connection"] != "Upgrade" or headers["Sec-WebSocket-Version"] != "13" or len(WebSocketKey) == 0:
                            raise KeyError("headers not Certain key.value")
                    except KeyError,e:#必须的key不存在,如果代码没错,小心nginx会导致没有Sec-WebSocket-Key
                        raise KeyError("websocket key error:" + str(e.message))
                    self.con.send(Util.calcResponseHandshake(WebSocketKey))
                    self.handshake = True
                    self.conObj["handshake"] = self.handshake
                else:
                    msg = self.con.recv(1024)
                    if msg == '':
                        raise RuntimeError("client close")
                    if self.g_code_length == 0:
                        self.g_code_length,self.g_header_length = Util.get_datalength(msg,self.g_code_length,self.g_header_length)
                    self.length_buffer += len(msg)
                    self.buffer_utf8 += msg
                    if self.length_buffer - self.g_header_length < self.g_code_length:
                        continue #数据未接收完,接续接受
                    msg = self.buffer_utf8
                    self.init()
                    self.branch(msg)
            except BaseException,e:
                self.init()
                logger.error("recv data error exe con.close ,info:" + traceback.format_exc())
                self.con.close()
                del self.cons[self.key]
                self.response("4", "")
                break

    #将消息分解开,并且处理沾包
    def branch(self,msg):
        hadelen = Util.t_headlen(msg)
        try:
            msglen = int(Util.t_recvStr(msg[0:hadelen + 5]))
        except ValueError:
            return ;
        codelen = 5 + 1 + msglen
        rowlen = hadelen + codelen
        nextMsg = msg[rowlen:]
        msg = Util.t_recvStr(msg[0:rowlen])
        if codelen != len(msg):
            return;
        if msg == '' or msg == False:
            raise RuntimeError("client close")
        # 数据接收完成,获取业务数据长度,前5个字节表示长度,与客户端定好
        type = msg[5:6]  # 操作符,长度后面的一个字节是操作符,与客户端定好
        msg = msg[6:]  # 消息内容,操作符后面至结束为业务数据
        retMsg = self.response(type, msg)
        Util.senOthers(retMsg, self.con)
        if nextMsg != '':  # 有沾包消息
            self.branch(nextMsg)

    #处理客户端发送来的消息
    def response(self,type,msg):
        ret = ""
        if type == "a": #心跳
            pass
        elif type == "0":  # 接收身份信息,返回身份id
            self.conObj["name"] = msg
            ret = str(self.key)
            self.response("5","")
        elif type == "1": # 收到请求获取其他用户列表
            keys = copy.deepcopy(self.cons.keys())
            keys.remove(self.key)
            #给用户加上是否在对话
            uids = []
            for key in keys:
                ready = 1 if key in self.ready else 0;
                if ready == 1: #检查是否在跟自己对话
                    ready = 2 if self.key in self.ready[key] else ready
                uids.append({"uid":key,"ready": ready})
            ret = json.dumps(uids)
        elif type == "2": #向另一个用户发起对话申请
            try:
                if msg not in self.ready.keys() and self.key not in self.ready.keys(): #必须是对方并自己,没有在对话才可以向对方发起对话
                    Util.senOthers(type + self.key, self.cons[msg]["con"])
                    self.ready[self.key] = []
                    self.ready[self.key].append(msg) #初始化自己的准备对象后,将对方的放入自己
                    self.ready[msg] = []
                    self.ready[msg].append(self.key) #初始化对方的准备对象后,将自己放入对方
                    self.response("5", "")
            except KeyError:
                pass
        elif type == "3": #用户响应另一个用户的对话请求
            try:
                if self.key in self.ready.keys(): #必须是双方已经被创建了准备对象才正确
                    uid = self.ready[self.key][0] #取出申请时服务端存储的对话准备初始化中的数据
                    if uid in self.ready.keys():
                        Util.senOthers(type + msg + self.key, self.cons[uid]["con"])
                        if msg == "1": #同意则将自己的id放入自己的对象中
                            self.ready[uid].append(uid)
                            self.ready[self.key].append(self.key)
                        elif msg == "0": #不同意则删除双方的对话对象
                            del self.ready[self.key]
                            del self.ready[uid]
                    self.response("5", "")
            except KeyError:
                pass
        elif type == "4": #一个用户向另一个用户取消对话申请
            try:
                if self.key in self.ready.keys():
                    uids = self.ready[self.key] #取出申请时服务端存储的对话准备初始化中的数据
                    for uid in uids:
                        if uid != self.key:
                            del self.ready[uid]
                            Util.senOthers(type + self.key, self.cons[uid]["con"]) #告诉对方我已经取消对话申请了
                        else:
                            del self.ready[self.key]
                            Util.senOthers(type + uid, self.cons[self.key]["con"])  # 通知自己关掉与对方的对话申请
            except KeyError:
                pass
            finally:
                self.response("5", "")# 不管取消是否成功都发一次最新的状态
        elif type == "5": #给每个在线的用户推一次当前在线用户列表
            for thisKey in self.cons.keys():
                keys = copy.deepcopy(self.cons.keys())
                keys.remove(thisKey)
                # 给用户加上是否在对话
                uids = []
                for k in keys:
                    ready = 1 if k in self.ready else 0;
                    if ready == 1:  # 检查是否在跟自己对话
                        ready = 2 if thisKey in self.ready[k] else ready
                    uids.append({"uid": k, "ready": ready})
                ret = json.dumps(uids)
                Util.senOthers("1" + ret, self.cons[thisKey]["con"])
        elif type == "6": #收到offer信令,发送给与他对话的用户
            try:
                for rd in self.ready[self.key]:
                    if rd != self.key:
                        obj = json.loads(msg);
                        obj["id"] = self.key;
                        Util.senOthers(type + json.dumps(obj), self.cons[rd]["con"])
            except KeyError:
                pass
        elif type == "7": #收到answer信令,响应给与他对话的用户
            try:
                for rd in self.ready[self.key]:
                    if rd != self.key:
                        obj = json.loads(msg);
                        obj["id"] = self.key;
                        Util.senOthers(type + json.dumps(obj), self.cons[rd]["con"])
            except KeyError:
                pass
        elif type == "8": #发送候选信息给对方
            try:
                for rd in self.ready[self.key]:
                    if rd != self.key:
                        Util.senOthers(type + msg, self.cons[rd]["con"])
            except KeyError:
                pass
        return type + ret


