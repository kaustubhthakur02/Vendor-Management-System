from django.shortcuts import render
from rest_framework import generics
from vendors.models import *
from vendors.serializers import *

class VendorInformation (generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorCRUD (generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "pk"

class PurchaseOrderDetails(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer