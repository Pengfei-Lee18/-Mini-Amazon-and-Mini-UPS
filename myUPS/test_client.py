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
from concurrent.futures import ProcessPoolExecutor
import world_ups_pb2 as World_Ups
import communication
import tools
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"


ip_port = ('vcm-25303.vm.duke.edu', 12345)

s = socket.socket()

s.connect(ip_port)

print("client send the message")
connect = communication.UConnect_obj()
tools.send_message(s, connect)

buf_message = tools.receive(s)
print(buf_message)
tmessage = World_Ups.UConnected()
tmessage.ParseFromString(buf_message)
print(tmessage)
id = tmessage.worldid
message ='server already receive the message: ' + str(id)
print(message)
while(1):
    pass
