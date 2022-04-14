#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj4.settings")
# import django
# if django.VERSION >= (1, 7):
#     django.setup()
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import world_ups_pb2 as World_Ups
ip_port = ('127.0.0.1', 12345)
import communication

sk = socket.socket()             
sk.bind(ip_port)                
sk.listen(5)                    
print('open socket and wait client to connect...')
conn, address = sk.accept()     
var_int_buff = []
while True:     # 
    while True:
        buf = conn.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    print(msg_len)
    buf_message = conn.recv(1024)
    tmessage = World_Ups.UConnected()
    tmessage.ParseFromString(buf_message)
    id = tmessage.worldid
    message ='server already receive the message: ' + str(id)
    conn.sendall(message.encode())    # feedback
    break
conn.close()    # close connection
