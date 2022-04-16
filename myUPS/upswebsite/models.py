from statistics import mode
from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique= True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name
    
class Truck(models.Model):
    truck_id = models.CharField(max_length=128, unique= True)
    truck_package_number = models.IntegerField(default=0)

class Package(models.Model):
    shipment_id = models.CharField(max_length=128, unique= True)
    tracking_id = models.AutoField(primary_key=True)
    dest = models.CharField(max_length=128, unique= True, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, blank=True)
    status_options = {
        ('pick_up','pick_up'),
        ('loading','loading'),
        ('delivering','delivering'),
        ('delivered','delivered'),
    }
    status = models.CharField(max_length=32, choices=status_options, default="pick_up")


# class Ack(models.Model):
#     seqnum = models.IntegerField(default=0)