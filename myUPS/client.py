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
import communication
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"


ip_port = ('127.0.0.1', 12345)

s = socket.socket()

s.connect(ip_port)

while True:
    print("client send the message")
    connect = communication.UConnect_obj()
    string_message = connect.SerializeToString()
    _EncodeVarint(s.send, len(string_message), None)
    s.send(string_message)


    server_reply = s.recv(1024).decode()
    print(server_reply)
    break
        
s.close()
