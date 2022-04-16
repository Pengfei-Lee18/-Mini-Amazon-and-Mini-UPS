import os
from unicodedata import name

from setuptools import Command 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "upswebsite.settings")
from django.db import transaction

import django 
if django.VERSION >= (1, 7):
    django.setup()
from upswebsite.models import DeliveringTruck, User,Package,Truck,Ack

from multiprocessing import cpu_count
import world_ups_pb2 as World_Ups
import UA_pb2 as UA
import client
import tools
seqnum = 0


##commuication with World_Ups
def UConnect_obj():
    connect = World_Ups.UConnect()
    # connect.worldid = int(input("please enter the worldid: ").strip())
    truck_raw_list = input("please enter the truck: ").split()
    truck_list =[truck_raw_list[i:i+3] for i in range(0,len(truck_raw_list),3)]
    
    for truck_num in truck_list:
        truck = connect.trucks.add()
        truck.id = int(truck_num[0])
        truck.x = int(truck_num[1])
        truck.y = int(truck_num[2])
    connect.isAmazon = False
    return connect


def UGoPickup_obj(truck_id,whid,seqnum): #truck_id, warehouse_id
    command = World_Ups.UCommands()
    command.pickups.append(
        command.UGoPickup(truck_id=truck_id,whid=whid,seqnum=seqnum)
    )
    return command

def UGoDeliver_obj(truck_id,package_id,x,y,seqnum): #truck_id, package_id, x, y
    command = World_Ups.UCommands()
    go_deliver = command.deliveries.add()
    go_deliver.truck_id = truck_id
    go_deliver.seqnum = seqnum
    location = go_deliver.packages.add()
    location.package_id = package_id
    location.x = x
    location.y = y
    return command

def Simspeed_obj(speed):
    command = World_Ups.UCommands()
    command.simspeed = speed
    return command

def UDisconnect_obj():
    command = World_Ups.UCommands()
    command.disconnect = True
    return command

def UQuery_obj(truck_id,seqnum):
    command = World_Ups.UCommands()
    query = command.queries.add()
    query.truck_id = truck_id
    query.seqnum = seqnum
    return command

def Ack_obj(seqnum):
    command = World_Ups.UCommands()
    ack = command.acks.add()
    ack.seqnum = seqnum
    return command

def UResponse_obj(buf_message):
    response = World_Ups.UResponse()
    response.ParseFromString(buf_message)
    for each_complete in response.completions:   #for pickup response
        truck = Truck.objects.get(id=each_complete.truck_id)
        delivering_truck = DeliveringTruck.objects.get(truck=truck)
        delivering_truck.delete()
        truck.status = 'loading'
        message = UsendArrive_obj(truck.truck_id)
        truck.save()
        # 发给amazon,改改socket
        tools.send_message(client.s,message)
        
    for each_delivered in response.delivered:
        truck = Truck.objects.get(id=each_delivered.truck_id)
        truck.status = 'delivered'
        truck.save()
        message = UpacDelivered_obj(each_delivered.shipment_id)
        #发给amazon,改改socket
        tools.send_message(client.s,message)
    for each_status in response.truckstatus:
        continue

    if response.HasField('finished'):
        if response.finished:
            closeworld()
    for each_ack in response.acks:
        ack = Ack.objects.create(seqnum=each_ack)
    for each_err in response.error:
        print(each_err.seqnum," error occur: ",each_err.error)

    return 

def closeworld():
    print("closeworld")
    client.s.close()
    return
#Communication with Amazon

def AResponse(buf_message):
    global seqnum
    response = UA.AUmessage()
    response.ParseFromString(buf_message)
    if response.HasField('pickup'):
        whid = response.pickup.whid
        shipment_id = response.pickup.shipment_id
        whid = response.pickup.whid
        if DeliveringTruck.objects.get(whid = whid).exists():
            truck = DeliveringTruck.objects.get(whid = whid).truck
        else:
            truck =Truck.objects.order_by('truck_package_number')[0]
            DeliveringTruck.objects.create(truck=truck,whid=whid)
        if response.pickup.HasField('ups_username'):
            if User.objects.get(name = username).exists():
                ups_username = response.pickup.ups_username
                package = Package.objects.create(shipment_id=shipment_id,user_id = ups_username,truck = truck,status = 'pick_up')
                response = UPacPickupRes_obj(package.tracking_id,package.truck.truck_id,package.shipment_id,True)
        else:
            package = Package.objects.create(shipment_id=shipment_id,truck = truck,status = 'pick_up')
            response = UPacPickupRes_obj(package.tracking_id,package.truck.truck_id,package.shipment_id,False)
        #给amazon端口发消息，改改socket
        tools.send_message(client.s,response)
        package.save()
        truck_id = truck.truck_id
        command = UGoPickup_obj(truck_id,whid,seqnum)
        seqnum += 1
        result = False
        while(not result):
            tools.send_message(client.s,command)
            result = Ack.objects.get(seqnum=seqnum).exists()
        

    if response.HasField('all_loaded'):
        truck_id = response.all_loaded.truck_id
        for package in response.all_loaded.packages:
            shipment_id = package.shipment_id
            package = Package.objects.get(shipment_id=shipment_id)
            package.status = 'delivering'
            package.save()
            command = UGoDeliver_obj(truck_id,shipment_id,package.x,package.y,seqnum)
            seqnum += 1
        result = False
        while(not result):
            tools.send_message(client.s,command)
            result = Ack.objects.get(seqnum=seqnum).exists()

    if response.HasField('bind_upsuser'):
        shipment_id = response.bind_upsuser.shipment_id
        username = response.bind_upsuser.ups_username
        package = Package.objects.get(shipment_id=shipment_id)
        if package.user_id == None:
            if User.objects.get(name = username).exists():
                package.user_id = response.bind_upsuser.ups_username
                bind_res = UBindRes_obj(shipment_id,True)
            else:
                bind_res = UBindRes_obj(shipment_id,False)
            package.save()
        #给amazon端口发消息，改改socket
        tools.send_message(client.s,bind_res)
        
    return

def USendWorldId_obj(worldid):
    message = UA.UAmessage()
    sendworld_id = message.world_id
    sendworld_id.world_id = worldid
    return message

def UPacPickupRes_obj(truck_id,is_binded,shipment_id,truck_id):
    message = UA.UAmessage()
    pickupres = message.pickup_res
    pickupres.truck_id = truck_id
    pickupres.is_binded = is_binded
    pickupres.shipment_id = shipment_id
    return message

def UsendArrive_obj(truck_id):
    message = UA.UAmessage()
    sendarrive = message.arrive
    sendarrive.truck_id = truck_id
    return message

def UpacDelivered_obj(shipment_id):
    message = UA.UAmessage()
    delivered = message.delivered
    delivered.shipment_id = shipment_id
    return message

def UBindRes_obj(shipment_id,is_binded):
    message = UA.UAmessage()
    bindres = message.bind_res
    bindres.shipment_id = shipment_id
    bindres.is_binded = is_binded
    return message

def UResendPackage_obj(shipment_id):
    message = UA.UAmessage()
    resendpackage = message.resend_package
    resendpackage.shipment_id = shipment_id
    return message

    