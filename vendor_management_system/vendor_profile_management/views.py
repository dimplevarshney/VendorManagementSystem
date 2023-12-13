from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from rest_framework import generics,status
from .serializers import VendorSerializer


class VendorListView(APIView):
    def get(self, request):  # Add 'pk=None' to the get method
        # print("17--",vendor_code)
        # # if kargs.get('vendor_code') is not None:
        # if vendor_code is not None:
        #     vendor = Vendor.objects.get(vendor_code=vendor_code)
        #     serializer = VendorSerializer(vendor)
        #     return Response(serializer.data)
        # else:
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetail(APIView):
    def get(self, request,  vendor_code=None):  # Add 'pk=None' to the get method
        print("17--",vendor_code)
        # if kargs.get('vendor_code') is not None:
        if vendor_code is not None:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)

    def put(self, request, vendor_code=None):  # Add 'vendor_code=None' to the put method
        if vendor_code is not None:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a valid Vendor ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_code=None):  # Add 'vendor_code=None' to the delete method
        if vendor_code is not None:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            vendors = Vendor.objects.all()
            vendors.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

