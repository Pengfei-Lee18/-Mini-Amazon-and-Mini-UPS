from multiprocessing import cpu_count
import world_ups_pb2 as World_Ups
seqnum = 0

def UConnect_obj():
    connect = World_Ups.UConnect()
    # connect.worldid = input("please enter the worldid: ").strip()
    truck_raw_list = input("please enter the truck: ").split()
    truck_list =[truck_raw_list[i:i+3] for i in range(0,len(truck_raw_list),3)]
    for truck in truck_list:
        connect.trucks.append(
            connect.UInitTruck(id=truck[0],x=truck[1],y=truck[2])
        )
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

