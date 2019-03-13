#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Util.py
# @Date  : 2019/2/21
# @User  : tanjun
# @Desc  : 工具类
import hashlib, base64
import struct

class Util:

    #使用客户端的key,生产响应的握手信息
    @staticmethod
    def calcResponseHandshake(clientKey):
        WebSocketKey = clientKey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        Ser_WebSocketKey = hashlib.sha1(WebSocketKey.encode(encoding='utf-8')).digest()
        Accept = base64.b64encode(Ser_WebSocketKey)  # 返回的是一个bytes对象
        handshake = "HTTP/1.1 101 Switching Protocols\r\n" \
                    "Connection: Upgrade\r\n" \
                    "Sec-WebSocket-Protocol: cat08" +"\r\n" \
                    "Sec-WebSocket-Accept: " + Accept.decode('utf-8') + "\r\n" \
                    "Upgrade: websocket\r\n\r\n"
        return handshake.encode(encoding='utf-8')

    #将数据发给指定的人
    @staticmethod
    def senOthers(msg,con):
        msg = Util.t_sendStr(msg)
        con.sendall(msg)

    #第一次连接进行客户端发起握手申请解析信息
    @staticmethod
    def t_header(buffer):
        buffer = buffer
        headers = {}
        # 对header进行分割后，取出后面的n-1个部分
        for line in buffer.split("\r\n")[1:]:  # 再对header 和 data部分进行单独的解析
            if line != '':
                key, value = line.split(": ", 1)  # 逐行的解析Request Header信息(Key,Value)
                headers[key] = value
        return headers

    #转换即将发送的数据
    @staticmethod
    def t_sendStr(data):
        if data:
            data = str(data)
        else:
            return False
        token = "\x81"
        length = len(data)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        # struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
        data = '%s%s' % (token, data)
        return data

    @staticmethod
    def t_headlen(info):
        payload_len = ord(info[1]) & 127  # 126以内是正确的长度
        if payload_len == 126:
            return 8
        elif payload_len == 127:
            return 14
        else:
            return 6

    #解析收到的数据
    @staticmethod
    def t_recvStr(info):
        payload_len = ord(info[1]) & 127 #126以内是正确的长度
        if payload_len == 126:
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            mask = info[10:14]
            decoded = info[14:]
        else:
            mask = info[2:6]
            decoded = info[6:]

        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = ord(decoded[i]) ^ ord(mask[i % 4])
            bytes_list.append(chunk)
        msg = str(bytes_list)
        return msg

    # 计算web端提交的数据长度并返回
    @staticmethod
    def get_datalength(msg,g_code_length,g_header_length):
        g_code_length = ord(msg[1]) & 127
        if g_code_length == 126:
            g_code_length = struct.unpack('>H', msg[2:4])[0]
            g_header_length = 8
        elif g_code_length == 127:
            g_code_length = struct.unpack('>Q', msg[2:10])[0]
            g_header_length = 14
        else:
            g_header_length = 6
        g_code_length = int(g_code_length)
        return g_code_length,g_header_length
