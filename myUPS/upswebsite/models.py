from django.db import models

# Create your models here.
class User(models.Model):
    gender = {
        ('male','male'),
        ('female','female'),
    }
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique= True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="male")
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Package(models.Model):
    shipment_id = models.CharField(max_length=128, unique= True)
    tracking_id = models.CharField(max_length=128, unique= True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status_options = {
        ('pick_up','pick_up'),
        ('loading','loading'),
        ('delivering','delivering'),
        ('delivered','delivered')
    }
    status = models.CharField(max_length=32, choices=status_options, default="pick_up")

class truck(models.Model):
    truck_id = models.CharField(max_length=128, unique= True)
    truck_package_number = models.IntegerField(default=0)
    