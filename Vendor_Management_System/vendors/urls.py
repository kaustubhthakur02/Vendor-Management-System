from django.urls import path,include
from .views import *
from . import views



urlpatterns = [
    path('vendor/', views.VendorInformation.as_view()),
    path('vendor/<int:pk>/', views.VendorCRUD.as_view()),
    path('purchase/', views.PurchaseOrderDetails.as_view()),
    path('purchase/<str:po_number>/', views.PurchaseCRUD.as_view()),
    path('demo/', views.demo),
    path('performance/<int:pk>/', views.VendorPerformanceAPIView.as_view()),

]