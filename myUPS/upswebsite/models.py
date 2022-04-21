from statistics import mode
from django.db import models

class World(models.Model):
    world_id = models.IntegerField(default=0)

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique= True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    world_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class Truck(models.Model):
    truck_id = models.AutoField(primary_key=True)
    truck_package_number = models.IntegerField(default=0)
    status_options = {
        ('idle','idle'),
        ('traveling','traveling'),
        ('arrive warehouse','arrive warehouse'),
        ('loading','loading'),
        ('delivering','delivering')
    }
    status = models.CharField(max_length=32, choices=status_options, default="idle")
    world_id = models.IntegerField(default=0)
     
class Package(models.Model):
    shipment_id = models.IntegerField(unique= True)
    tracking_id = models.AutoField(primary_key=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, blank=True)
    status_options = {
        ('pick_up','pick_up'),
        ('loading','loading'),
        ('delivering','delivering'),
        ('delivered','delivered'),
    }
    status = models.CharField(max_length=32, choices=status_options, default="pick_up")
    world_id = models.IntegerField(default=0)
    
class DeliveringTruck(models.Model):
    whid = models.IntegerField(primary_key=True)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, blank=True)
    world_id = models.IntegerField(default=0)
    def __str__(self):
        return self.truck.truck_id

class Ack(models.Model):
    seqnum = models.IntegerField(default=0)
    world_id = models.IntegerField(default=0)

class Sequence(models.Model):
    seq = models.IntegerField(default=0)
    world_id = models.IntegerField(default=0)

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=128)
    count = models.IntegerField(default=0)
    shipment_id = models.IntegerField(default=0)
    world_id = models.IntegerField(default=0)

