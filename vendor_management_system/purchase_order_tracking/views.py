from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import PurchaseOrderSerializer
from .models import *


class PurchaseOrderListView(APIView):
    def get(self, request): 
        vendor = request.GET.get("vendor")
        if vendor is not None:
            purchase = PurchaseOrder.objects.filter(vendor = vendor)
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
    def get(self, request,  po_number=None):
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            serializer = PurchaseOrderSerializer(purchase)
            return Response(serializer.data)
        else:
            purchase = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase, many=True)
            return Response(serializer.data)

    def put(self, request, po_number=None):
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            po_serializer = PurchaseOrderSerializer(purchase, data=request.data)
            if po_serializer.is_valid():
                po_serializer.save()
                return Response(po_serializer.data)
            return Response(po_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid PurchaseId.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_number=None):
        if po_number is not None:
            purchase = PurchaseOrder.objects.get(po_number=po_number)
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            purchase = PurchaseOrder.objects.all()
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

