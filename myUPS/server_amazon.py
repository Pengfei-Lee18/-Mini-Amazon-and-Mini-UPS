#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj4.settings")
# import django
# if django.VERSION >= (1, 7):
#     django.setup()
import socket
import time
import tools
import UA_pb2 as UA
# connected = World_Ups.UConnected()
# connected.worldid = 1
# connected.result = "OK"

'''
insert into warehouse (wh_id, x,y, world_id) values (1,222,223,1);
insert into package (package_id , wh_id , world_id , truck_id , desx , desy , package_status) values (1,1,1,1,2,3,'LOADED');
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

message = UA.AUmessage()
pickup_message = message.pickup
pickup_message.whid = 1
pickup_message.x = 2
pickup_message.y = 3
pickup_message.shipment_id = 1
pickup_message.ups_username = 'test'
tools.send_message(s,message)


buf_message = tools.receive(s)
print(buf_message)
tmessage2 = UA.UAmessage()
tmessage2.ParseFromString(buf_message)
pickupres = tmessage2.pickup_res
print(pickupres)
truckid = pickupres.truck_id
print(truckid)
print('server already receive the message: ' )
print(tmessage2)


buf_message2 = tools.receive(s)
print(buf_message2)
tmessage2 = UA.UAmessage()
tmessage2.ParseFromString(buf_message2)
print('server already receive the message: ' )
print(tmessage2)



# bind
message = UA.AUmessage()
print('client send the message for bind_upsuser')
bind_upsuser = message.bind_upsuser
bind_upsuser.shipment_id = 1
bind_upsuser.ups_username = 'feifei'
tools.send_message(s,message)
buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
tmessage.ParseFromString(buf_message)
print('server already receive the message: ' )
print(tmessage)



message = UA.AUmessage()
all_loaded = message.all_loaded
#??????????????????
all_loaded.truck_id = truckid
print(truckid)
package = all_loaded.packages.add()
package.x = 2
package.y = 3
package.shipment_id = 1
item = package.item.add()
item.product_id = 1
item.description = 'test_product_description'
item.count = 2
print(message)
tools.send_message(s,message)
buf_message = tools.receive(s)
print(buf_message)
tmessage = UA.UAmessage()
tmessage.ParseFromString(buf_message)
print('server already receive the message: ' )
print(tmessage)
time.sleep(5)




while True:
    pass
s.close()

