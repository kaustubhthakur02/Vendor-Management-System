from rest_framework import serializers
from vendors.models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        extra_kwargs = {
            'order_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'delivery_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'issue_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'acknowledgment_date': {'format': '%Y-%m-%dT%H:%M:%S'},
        }

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'