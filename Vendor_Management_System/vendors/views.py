from django.shortcuts import render
from rest_framework import generics
from vendors.models import *
from vendors.serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, status

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

class PurchaseCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = "po_number"
    print(PurchaseSerializer)

def demo(request):
    return render(request, 'index.html',)

