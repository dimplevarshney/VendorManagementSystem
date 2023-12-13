from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorPerformanceSerializer
from purchase_order_tracking.serializers import PurchaseOrderSerializer
from .models import *
from purchase_order_tracking.models import PurchaseOrder

# Create your views here.
class VendorPerformanceDetails(APIView):
    def get(self,request,vendor=None):
        if vendor is not None:
            performance = HistoricalPerformance.objects.filter(vendor = vendor)
            serializer = VendorPerformanceSerializer(performance,many=True)
            return Response(serializer.data)

            

