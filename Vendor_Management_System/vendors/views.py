from django.shortcuts import render
from rest_framework import generics
from vendors.models import *
from vendors.serializers import *
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.response import Response

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


def demo(request):
    return render(request, 'index.html')


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate performance metrics
        on_time_delivery_rate = calculate_on_time_delivery_rate(instance)
        quality_rating_avg = calculate_quality_rating_avg(instance)
        average_response_time = calculate_average_response_time(instance)
        fulfillment_rate = calculate_fulfillment_rate(instance)

        # Store historical data
        store_historical_data(instance, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate)

        data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return Response(data)

def calculate_on_time_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed_orders = completed_orders.count()

    if total_completed_orders == 0:
        return 0

    on_time_deliveries = completed_orders.filter(delivery_date__lte=timezone.now()).count()

    on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100
    return round(on_time_delivery_rate, 2)

def calculate_quality_rating_avg(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    total_completed_orders = completed_orders.count()

    if total_completed_orders == 0:
        return 0

    quality_ratings = completed_orders.aggregate(avg_rating=models.Avg('quality_rating'))
    quality_rating_avg = quality_ratings['avg_rating']
    return round(quality_rating_avg, 2) if quality_rating_avg else 0

def calculate_average_response_time(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)

    if not completed_orders.exists():
        return 0

    total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_orders)
    average_response_time = total_response_time / completed_orders.count()
    return round(average_response_time / 3600, 2)  # Convert seconds to hours

def calculate_fulfillment_rate(vendor):
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()

    if total_orders == 0:
        return 0

    successful_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    fulfillment_rate = (successful_orders.count() / total_orders) * 100
    return round(fulfillment_rate, 2)

def store_historical_data(vendor, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate):
    # Store historical data in the database
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now().date(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate
    )