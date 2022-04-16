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

def send_message(s, message):
    string_message = message.SerializeToString()
    _EncodeVarint(s.send, len(string_message), None)
    s.send(string_message)

def receive(s):
    var_int_buff = []
    while True:
        buf = s.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    print(msg_len)
    buf_message = s.recv(msg_len)
    return buf_message