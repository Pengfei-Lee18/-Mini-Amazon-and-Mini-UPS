import ece568finalproj.myUPS.world_ups_pb2 as World_Ups

# create an Order instance
connected = World_Ups.UConnected()

connected.worldid = 1
connected.result = "OK"

print(connected)