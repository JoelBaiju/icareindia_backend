from django.db import models
from django.contrib.auth.models import User
from Users import models as Users_models


class TechnicianProfile(models.Model):
    phone=models.CharField(max_length=50 ,blank=True)
    alt_phone=models.CharField(max_length=15,blank=True)
    gender=models.CharField(max_length=15 , blank=True)
    lattitude = models.DecimalField(max_digits=15, decimal_places=11, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=11, blank=True, null=True)
    addressline = models.CharField( max_length=100,blank=True,default='',null=True)
    userObj=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20,blank=True) 
    isworking=models.BooleanField(default=True)
    image = models.ImageField(upload_to='Technician_images/',blank=True,null=True,default='')
    deviceid=models.CharField(max_length=200,blank=True,null=True)

    
    
class TechniciansEarnings(models.Model):
    date=models.DateField()
    earnings=models.IntegerField(default=0)
    technician=models.ForeignKey(TechnicianProfile,on_delete=models.CASCADE)
    
    
    
class Schedule(models.Model):
    date=models.DateField(blank=True)
    am8=models.IntegerField(blank=True)
    am9=models.IntegerField(blank=True)
    am10=models.IntegerField(blank=True)
    am11=models.IntegerField(blank=True)
    am12=models.IntegerField(blank=True)
    pm1=models.IntegerField(blank=True)
    pm2=models.IntegerField(blank=True)
    pm3=models.IntegerField(blank=True)
    pm4=models.IntegerField(blank=True)
    pm5=models.IntegerField(blank=True)
    pm6=models.IntegerField(blank=True)
    pm7=models.IntegerField(blank=True)


  
