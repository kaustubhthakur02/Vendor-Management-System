from django.urls import path,include
from . import views

urlpatterns = [
    path('vendor/', views.VendorInformation.as_view()),
    path('vendor/<int:pk>/', views.VendorCRUD.as_view()),
    path('purchase/', views.PurchaseOrderDetails.as_view())
]