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
connected = World_Ups.UConnected()
connected.worldid = 1
connected.result = "OK"

string_message = connected.SerializeToString()
ip_port = ('127.0.0.1', 12345)

s = socket.socket()     # 

s.connect(ip_port)      # 

while True:
    print("client send the message")     # 
    # inp = input("please enter the send message: ").strip()
    # if not inp:     
    #     continue
    # inp = open('testxml').read()
    _EncodeVarint(s.send, len(string_message), None)
    s.send(string_message)

    # if inp == "exit":   # 
    #     print("close connection!")
    #     break
    server_reply = s.recv(1024).decode()
    print(server_reply)
    break
        
s.close()
