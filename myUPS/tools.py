#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import socket
# from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
# from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint32
import world_ups_pb2 as World_Ups
import communication
import struct
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"
import threading
import time
lock=threading.Lock()
lock1=threading.Lock()

def send_message(s, message):
    string_message = message.SerializeToString()
    _EncodeVarint(s.send, len(string_message), None)
    s.send(string_message)
    # time.sleep(0.01)


def receive(s):
    # lock1.acquire() 
    var_int_buff = []
    while True:
        try:
            buf = s.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break
        except IndexError as ex:
            continue
    print(msg_len)
    buf_message = s.recv(msg_len)
    # lock1.release() 
    return buf_message


# def send_message(socket,msg):
#     string = msg.SerializeToString()
#     data = []
#     _EncodeVarint()(data.append, len(string), None)
#     size = b''.join(data)
#     socket.sendall(size + string)

# def receive(s):
#     data = b''
#     data += s.recv(1)
#     size = _DecodeVarint32(data, 0)[0]
#     string = s.recv(size)
#     return string
