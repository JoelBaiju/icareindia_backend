from django.db import models



class Razorpay(models.Model):
    key=models.CharField(max_length=50,null=True)
    