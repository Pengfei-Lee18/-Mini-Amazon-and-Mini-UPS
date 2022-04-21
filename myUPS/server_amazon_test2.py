#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj4.settings")
# import django
# if django.VERSION >= (1, 7):
#     django.setup()
import socket
import time
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
from concurrent.futures import ProcessPoolExecutor
import world_ups_pb2 as World_Ups
import communication
import tools
import UA_pb2 as UA
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"
'''
4.如果所有的车在去warehouse的路上 但我需要一辆新的车去另一个warehouse

测试案例： initialize 一辆车去A 但我马上收到另一个请求要求去B
insert into warehouse (wh_id, x,y, world_id) values (1,1100,1100,1);
insert into warehouse (wh_id, x,y, world_id) values (2,1600,1600,1);
insert into package (package_id , wh_id , world_id , truck_id , desx , desy , package_status) values (1,1,1,1,3020,3030,'LOADED');
insert into package (package_id , wh_id , world_id , truck_id , desx , desy , package_status) values (2,2,1,1,3120,3130,'LOADED');
'''


ip_port = ('127.0.0.1', 55555)

s = socket.socket()

s.connect(ip_port)

print("client send the message")
# connect = communication.UConnect_obj()
# tools.send_message(s, connect)

buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
tmessage.ParseFromString(buf_message)
print('server already receive the message: ' )
print(tmessage)  
time.sleep(3)

#pickup 1
message = UA.AUmessage()
pickup_message = message.pickup
pickup_message.whid = 1
pickup_message.x = 3020
pickup_message.y = 3030
pickup_message.shipment_id = 1
pickup_message.ups_username = 'test'
tools.send_message(s,message)

buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
pickupres = tmessage.pickup_res
truckid = pickupres.truck_id
tmessage.ParseFromString(buf_message)

print('server already receive the message for pickup package 1: ' )
print(tmessage)

#pickup 2
message = UA.AUmessage()
pickup_message = message.pickup
pickup_message.whid = 2
pickup_message.x = 3120
pickup_message.y = 3130
pickup_message.shipment_id = 2
pickup_message.ups_username = 'test'
tools.send_message(s,message)



#pickup 1 arrive warehouse
buf_message2 = tools.receive(s)
print(buf_message2)
tmessage2 = UA.UAmessage()
tmessage2.ParseFromString(buf_message2)
print('server already receive the message for arrive warehouse1: ' )
print(tmessage2)


#send truck 1 all loaded
message = UA.AUmessage()
all_loaded = message.all_loaded
all_loaded.truck_id = 1
package = all_loaded.packages.add()
package.x = 3020
package.y = 3030
package.shipment_id = 1
item = package.item.add()
item.product_id = 1
item.description = 'test_product_description'
item.count = 3
tools.send_message(s,message)



#有可用的卡车，我们可以收到Pickup2 response
buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
pickupres = tmessage.pickup_res
truckid = pickupres.truck_id
tmessage.ParseFromString(buf_message)

print('server already receive the message for pickup package 2: ' )
print(tmessage)


#pickup 2 arrive warehouse
buf_message3 = tools.receive(s)
print(buf_message3)
tmessage3 = UA.UAmessage()
tmessage3.ParseFromString(buf_message3)
print('server already receive the message for arrive warehouse 2: ' )
print(tmessage3)

#发第二个的load

message = UA.AUmessage()
all_loaded = message.all_loaded
all_loaded.truck_id = 1
package = all_loaded.packages.add()
package.x = 3120
package.y = 3130
package.shipment_id = 2
item = package.item.add()
item.product_id = 2
item.description = 'test_product_description2'
item.count = 2
tools.send_message(s,message)

#delivered 1
buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
tmessage.ParseFromString(buf_message)
print('server already receive the message delivered package 1: ' )
print(tmessage)

#delivered 2
buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
tmessage.ParseFromString(buf_message)
print('server already receive the message delivered package 2: ' )
print(tmessage)





# message = UA.AUmessage()
# print('client send the message for bind_upsuser')
# bind_upsuser = message.bind_upsuser
# bind_upsuser.shipment_id = 1
# bind_upsuser.ups_username = 'test1'
# tools.send_message(s,message)
# time.sleep(15)
# buf_message = tools.receive(s)
# print(buf_message)
# tmessage = UA.UAmessage()
# tmessage.ParseFromString(buf_message)
# print('server already receive the message: ' )
# print(tmessage)
while True:
    pass
s.close()

