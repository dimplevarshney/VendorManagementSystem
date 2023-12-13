from django.db import models
from vendor_profile_management.models import Vendor
from datetime import datetime,time


# Create your models here.
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20,primary_key=True)
    vendor= models.ForeignKey(Vendor,on_delete=models.CASCADE,default=1)
    order_date = models.DateTimeField(null=False,default=datetime.combine(datetime.today(), time.min)) #Date when the order was placed.
    delivery_date = models.DateTimeField(null=False) #Expected or actual delivery date of the order.
    items = models.JSONField(null=False) #Details of items ordered.
    quantity = models.IntegerField(null=False,default=0) #Total quantity of items in the PO.
    status = models.CharField(max_length=20,null=False,choices=(('pending','pending'),('completed','completed'),('canceled','canceled')),default='pending') #Current status of the PO (e.g., pending, completed, canceled).
    quality_rating = models.FloatField(max_length=10,null=True,default=0.0)  #Rating given to the vendor for this PO (nullable).
    issue_date = models.DateTimeField(null=False,default=datetime.combine(datetime.today(), time.min)) #Timestamp when the PO was issued to the vendor.
    acknowledgment_date = models.DateTimeField(null=True) #Timestamp when the vendor acknowledged the PO.

