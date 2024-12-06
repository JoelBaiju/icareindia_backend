from django.db import models
from django.contrib.auth.models import User
from Technicians import models as technicianmodel


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    alt_phone= models.CharField(max_length=15, blank=True)
    gender=models.CharField(max_length=20,blank=True)
    name=models.CharField(max_length=50,blank=True)
    def __str__(self):
            return self.name


class UserAddress(models.Model):
    addressline=models.CharField( max_length=100,blank=True)
    longitude=models.CharField(max_length=50,blank=True)
    lattitude=models.CharField(max_length=50,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
class UserTokens(models.Model):
    user_token=models.CharField(max_length=100,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductsMainCategories(models.Model):
    categoryname=models.CharField(max_length=50,blank=True)
    image=models.ImageField(upload_to='Main_category_images/')
    managedbyadmin=models.BooleanField(default=False)
    
class ProductSubcategories (models.Model):
    categoryname=models.CharField(max_length=50,blank=True)
    description=models.CharField(max_length=500,blank=True)
    maincategory=models.ForeignKey(ProductsMainCategories,on_delete=models.CASCADE)
    
class SearchKeyWords (models.Model):
    keyword=models.CharField(max_length=50,blank=True)
    subcategory=models.ForeignKey(ProductSubcategories, on_delete=models.CASCADE)
    

class Issues (models.Model):
    issue=models.CharField(max_length=300,default='_')
    time=models.CharField(blank=True,max_length=20,null=True)
    date=models.DateField(blank=True,null=True)
    status=models.CharField(blank=True,max_length=50,null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    technician=models.ForeignKey(technicianmodel.TechnicianProfile,on_delete=models.CASCADE,blank=True,null=True)
    subcategory=models.ForeignKey(ProductSubcategories,on_delete=models.CASCADE,null=True)
    audio=models.FileField(upload_to='Issue_Audios/' ,null=True)
    sparecost=models.CharField(default='-',max_length=50)
    servicecost=models.CharField(default='-',max_length=50)
    totalcost=models.CharField(default='-',max_length=50)
    technicianremark=models.CharField(default='_',max_length=5000)
    managedbyadmin=models.BooleanField(default=False)
    
    
    
class Tickets(models.Model):
    ticket=models.CharField(blank=True,max_length=10000,null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    issue=models.ForeignKey(Issues,on_delete=models.CASCADE)
    


class TechnicianAcceptedServices(models.Model):
    category=models.ForeignKey(ProductsMainCategories,on_delete=models.CASCADE)
    technician=models.ForeignKey(technicianmodel.TechnicianProfile , on_delete=models.CASCADE)