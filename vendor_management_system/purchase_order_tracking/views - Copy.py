from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import PurchaseOrderSerializer
from .models import *
from vendor_profile_management.serializers import VendorSerializer
from vendor_profile_management.models import Vendor
from vendor_performance_evaluation.serializers import VendorPerformanceSerializer
from vendor_performance_evaluation.models import HistoricalPerformance
import traceback
from django.db.models import Avg,F, ExpressionWrapper, fields,Sum
from django.utils import timezone


class PurchaseOrderListView(APIView):
    def get(self, request):  # Add 'pk=None' to the get method
        vendor = request.GET.get("vendor")
        print(vendor)
        if vendor is not None:
            purchase = PurchaseOrder.objects.filter(vendor = vendor)
            # purchase = PurchaseOrder.objects.get(vendor = vendor)
            print(purchase)
        else:
            purchase = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetail(APIView):
    def get(self, request,  po_number=None):  # Add 'pk=None' to the get method
        print("17--",po_number)
        # if kargs.get('po_number') is not None:
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            serializer = PurchaseOrderSerializer(purchase)
            return Response(serializer.data)
        else:
            purchase = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase, many=True)
            return Response(serializer.data)

    def put(self, request, po_number=None):
        print("50--",po_number)
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            po_serializer = PurchaseOrderSerializer(purchase, data=request.data)
            
            if po_serializer.is_valid():
                po_serializer.save()
                if request.data['status']== 'completed':
                    vendor = request.data['vendor']
                    vendor_data = Vendor.objects.get(vendor_code = vendor)
                    
                    #On-Time Delivery Rate:
                    delivery_date = purchase.delivery_date
                    total_complete_count = PurchaseOrder.objects.filter(vendor=vendor,status="completed").count()
                    complete_before_delivery = PurchaseOrder.objects.filter(vendor=vendor,status="completed", delivery_date__lte=delivery_date).count()
                    if total_complete_count != 0:
                        on_time_delivery_rate = complete_before_delivery / total_complete_count
                    else:
                        on_time_delivery_rate = 0
                    vendor_data.on_time_delivery_rate = on_time_delivery_rate
                    
                    #Quality Rating Average:
                    if request.data['quality_rating']:
                        avg_quality_rate = PurchaseOrder.objects.filter(vendor=vendor,status='completed').aggregate(avg_quality_rate = Avg('quality_rating'))
                    vendor_data.quality_rating_avg = avg_quality_rate['avg_quality_rate']

                    #Fulfilment Rate:
                    total_complete_count = PurchaseOrder.objects.filter(vendor=vendor,status="completed").count()
                    total_order_count = PurchaseOrder.objects.filter(vendor=vendor).count()
                    fulfillment_rate = total_complete_count / total_order_count
                    vendor_data.fulfillment_rate = fulfillment_rate

                    vendor_serializer = VendorSerializer(vendor_data,data={"on_time_delivery_rate" : on_time_delivery_rate},partial = True)
                    if vendor_serializer.is_valid():
                        vendor_serializer.save()
                    

                if request.data['acknowledgment_date']:
                    vendor = request.data['vendor']
                    print("57--",vendor)
                    vendor_data = Vendor.objects.get(vendor_code = vendor)
                    orders_with_date_difference = PurchaseOrder.objects.filter(vendor=vendor).annotate(
                            date_difference=ExpressionWrapper(
                                F('acknowledgment_date') - F('issue_date'),
                                output_field=fields.DurationField()
                            )
                        )

                    print(orders_with_date_difference)
                    # for order in orders_with_date_difference:
                    #     print(f"Order #{order.po_number}: Date Difference - {order.date_difference}")
                    #     diff_total = diff_total + order.date_difference
                    # print(diff_total)
                    total_order_count = PurchaseOrder.objects.filter(vendor=vendor).count()

                    diff_total = orders_with_date_difference.aggregate(Sum('date_difference'))['date_difference__sum'].total_seconds() if orders_with_date_difference.exists() else 0
                    total_order_count = orders_with_date_difference.count()
                    print("109--",diff_total)
                    if total_order_count != 0:
                        avg_response_time = diff_total / total_order_count
                    else:
                        avg_response_time = 0
                    print("114--",avg_response_time)
                    vendor_data.average_response_time = avg_response_time
                    vendor_serializer = VendorSerializer(vendor_data,data={"average_response_time" : avg_response_time},partial = True)

                    if vendor_serializer.is_valid():
                        vendor_serializer.save()
                    
                # po_serializer.save()
                return Response(po_serializer.data)
            return Response(po_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a valid Vendor ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_number=None):
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            purchase = PurchaseOrder.objects.all()
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

