from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg, ExpressionWrapper, F, fields, Sum
from django.core.exceptions import ObjectDoesNotExist
# from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from .models import *
from vendor_profile_management.serializers import VendorSerializer
from vendor_profile_management.models import Vendor
from vendor_performance_evaluation.serializers import VendorPerformanceSerializer
from vendor_performance_evaluation.models import HistoricalPerformance

#Signal Functionality to calculate PerformanceMetrices in Vendor after updating PurchaseOrder
@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor_id = instance.vendor.vendor_code
        vendor_data = Vendor.objects.get(vendor_code = vendor_id)
        
        #On-Time Delivery Rate:
        delivery_date = instance.delivery_date
        total_complete_count = PurchaseOrder.objects.filter(vendor=vendor_id,status="completed").count()
        complete_before_delivery = PurchaseOrder.objects.filter(vendor=vendor_id,status="completed", delivery_date__lte=delivery_date).count()
        if total_complete_count != 0:
            on_time_delivery_rate = complete_before_delivery / total_complete_count
        else:
            on_time_delivery_rate = 0
        vendor_data.on_time_delivery_rate = on_time_delivery_rate

        #Quality Rating Average:
        if instance.quality_rating:
            avg_quality_rate = PurchaseOrder.objects.filter(vendor=vendor_id,status='completed').aggregate(avg_quality_rate = Avg('quality_rating'))
        vendor_data.quality_rating_avg = avg_quality_rate['avg_quality_rate']
        
        #Fulfilment Rate:
        total_complete_count = PurchaseOrder.objects.filter(vendor=vendor_id,status="completed").count()
        total_order_count = PurchaseOrder.objects.filter(vendor=vendor_id).count()
        fulfillment_rate = total_complete_count / total_order_count
        vendor_data.fulfillment_rate = fulfillment_rate

        vendor_serializer = VendorSerializer(vendor_data,data={"on_time_delivery_rate" : on_time_delivery_rate},partial = True)
        if vendor_serializer.is_valid():
            vendor_serializer.save()

    #Average Response Time
    if instance.acknowledgment_date:
        vendor_id = instance.vendor.vendor_code
        vendor_data = Vendor.objects.get(vendor_code = vendor_id)
        orders_with_date_difference = PurchaseOrder.objects.filter(vendor=vendor_id).annotate(
                date_difference=ExpressionWrapper(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=fields.DurationField()
                )
            )

        total_order_count = PurchaseOrder.objects.filter(vendor=vendor_id).count()
        diff_total = orders_with_date_difference.aggregate(Sum('date_difference'))['date_difference__sum'].total_seconds() if orders_with_date_difference.exists() else 0
        total_order_count = orders_with_date_difference.count()
        if total_order_count != 0:
            avg_response_time = diff_total / total_order_count
        else:
            avg_response_time = 0

        vendor_data.average_response_time = avg_response_time
        vendor_serializer = VendorSerializer(vendor_data,data={"average_response_time" : avg_response_time},partial = True)
        if vendor_serializer.is_valid():
            vendor_serializer.save()
                   
#Signal triggers after PurchaseOrder gets saved
post_save.connect(calculate_on_time_delivery_rate, sender=PurchaseOrder)

#Signal Functionality to create a record in HistoricalPerformance each time vendor gets updated
@receiver(post_save,sender=Vendor)
def fill_historical_performance(sender,instance,**kwargs):
    print("called")
    performance_serializer = VendorPerformanceSerializer(data={"vendor":instance.vendor_code,"date":timezone.now(),"on_time_delivery_rate":instance.on_time_delivery_rate,"quality_rating_avg":instance.quality_rating_avg,"average_response_time":instance.average_response_time,"fulfillment_rate":instance.fulfillment_rate})
    if performance_serializer.is_valid():
        performance_serializer.save()

#Signal triggers after Vendors gets saved
post_save.connect(fill_historical_performance,sender=Vendor)
