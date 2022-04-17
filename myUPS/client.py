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
import world_ups_pb2 as World_Ups
import communication
import tools
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"

def runamz(s, conn):
    pools = ProcessPoolExecutor(20)
    while True: 
        resp_message = tools.receive(conn)
        pools.submit(communication.AResponse, resp_message, s, conn)
        pools.submit()

def runworld(s, conn):
    pools = ProcessPoolExecutor(20)
    while True: 
        resp_message = tools.receive(s)
        pools.submit(communication.UResponse_obj, resp_message, s, conn)
        pools.submit()

ip_port = ('vcm-25303.vm.duke.edu', 23456)
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
ID = tmessage.worldid
message ='server already receive the message: ' + str(ID)
print(message)

#连接amz,并告诉amz worldid
server_port = ('vcm-26404.vm.duke.edu', 54321)
sk = socket.socket()             
sk.bind(server_port)                
sk.listen(5)                    
print('open socket and wait client to connect...')
conn, address = sk.accept()     
var_int_buff = []
tools.send_message(conn, ID)

#开两个进程
#一个是处理amz
print('Parent process %s.' % os.getpid())
p1 = Process(target=runamz, args=(s,conn))
print('Child process will start.')
p1.start()

#一个是处理world
print('Parent process %s.' % os.getpid())
p2 = Process(target=runworld, args=(s,conn))
print('Child process will start.')
p2.start()

p1.join()
p2.join()
s.close()
conn.close()
print('Child process end.')

