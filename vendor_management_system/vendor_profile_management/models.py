from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=50,null=False)
    contact_details = models.IntegerField(null=False)
    address = models.CharField(max_length=150,null=False)
    on_time_delivery_rate = models.FloatField(max_length=10,null=False,default=0.0) 
    quality_rating_avg = models.FloatField(max_length=10,null=False,default=0.0)
    average_response_time = models.FloatField(max_length=10,null=False,default=0.0)
    fulfillment_rate = models.FloatField(max_length=10,null=False,default=0.0) 

