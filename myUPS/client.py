#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from multiprocessing import Process
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myUPS.settings")
# import django
# if django.VERSION >= (1, 7):
#     django.setup()
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import world_ups_pb2 as World_Ups
import UA_pb2 as UA
import communication
import tools
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"

def runamz(s, conn):
    pools = ThreadPoolExecutor(20)
    while True: 
        resp_message = tools.receive(conn)
        print("client receive the message from amz:")
        print(resp_message,s,conn)
        pools.submit(communication.AResponse, resp_message, s, conn)

def runworld(s, conn):
    pools = ThreadPoolExecutor(20)
    while True: 
        resp_message = tools.receive(s)
        print("client receive the message from world:")
        print(resp_message,s,conn)
        pools.submit(communication.UResponse_obj, resp_message, s, conn)

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
world_id = tmessage.worldid
message ='server already receive the message: ' + str(world_id)
print(message)

#连接amz,并告诉amz worldid
server_port = ('0.0.0.0', 55555)
sk = socket.socket()             
sk.bind(server_port)                
sk.listen(5)                    
print('open socket and wait client to connect...')
conn, address = sk.accept()     
var_int_buff = []
message = UA.UAmessage()
Id = message.world_id 
Id.world_id = world_id
tools.send_message(conn, message)

#开两个进程
#一个是处理amz
thread1 = threading.Thread(target=runamz, args=(s,conn,))

#一个是处理world
thread2 = threading.Thread(target=runworld, args=(s,conn,))

thread1.start()
thread2.start()
thread1.join()
thread2.join()
s.close()
conn.close()
print('Child process end.')

