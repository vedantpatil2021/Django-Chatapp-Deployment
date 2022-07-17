from django.db import models
from datetime import datetime 
# Create your models here.

class Room(models.Model):
    roomname   = models.CharField(max_length=100)
    phone      = models.CharField(max_length=12,blank=True)
    adminname  = models.CharField(max_length=50,blank=True)
    blockuser = models.TextField(blank=True)

    def __str__(self):
        return self.roomname

class Message(models.Model):
    value =  models.CharField( max_length=10000)
    date  =  models.DateTimeField( default=datetime.now ,blank=True)
    user  = models.CharField(max_length=10000)
    roomname  = models.CharField(max_length=1000)
    phone     = models.CharField(max_length=12,blank=True)
    
    def __str__(self):
        return self.user
