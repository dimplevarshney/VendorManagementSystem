from django.db import models
from vendor_profile_management.models import Vendor

# Create your models here.
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete= models.CASCADE,default=0) #ForeignKey - Link to the Vendor model.
    date = models.DateTimeField(null=False) #Date of the performance record.
    on_time_delivery_rate = models.FloatField(max_length=10,null=False,default=0.0) #Historical record of the on-time delivery rate.
    quality_rating_avg = models.FloatField(max_length=10,null=False,default=0.0) #Historical record of the quality rating average.
    average_response_time = models.FloatField(max_length=10,null=False,default=0.0) #Historical record of the average response time.
    fulfillment_rate = models.FloatField(max_length=10,null=False,default=0.0) #Historical record of the fulfilment rate.
