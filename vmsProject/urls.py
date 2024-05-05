"""
URL configuration for vmsProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# import vendorAPI
from vmsApp.apis import VendorViewsAPI, VendorListAPI, VendorPerformanceView
from vmsApp.apis import PurchaseOrderAPI, PurchasedOrderViewAPI
from vmsApp.apis import OrderAcknowledgeAPI, CompletePurchaseOrderAPI, UpdatePurchaseOrderQualityRatingAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    # Vender API
    path('api/vendors/', VendorListAPI.as_view(), name='create_new_vendor & list_all_vendors'),
    path('api/vendors/<uuid:vendor_id>/', VendorViewsAPI.as_view(), name="retrieve_update_and_delete_vendor's_details"),
    path('api/vendors/<uuid:vendor_id>/performance/', VendorPerformanceView.as_view(), name='get_vendor_performance'),

    # Purchase Order API
    path('api/purchase_orders/', PurchaseOrderAPI.as_view(), name='create_new_order & list_all_purchase_orders'),
    path('api/purchase_orders/<uuid:po_id>/', PurchasedOrderViewAPI.as_view(), name='retrieve_update_and_delete_purchase_orders'),

    # Common API
    path('api/purchase_orders/<uuid:po_id>/acknowledge/', OrderAcknowledgeAPI.as_view(), name='acknowledge_purchase_orders'),
    path('api/purchase_orders/<uuid:po_id>/complete/', CompletePurchaseOrderAPI.as_view(), name='complete_purchase_order'),
    path('api/purchase_orders/<uuid:po_id>/quality_rating/', UpdatePurchaseOrderQualityRatingAPI.as_view(), name='give_quality_rating_on_purchased_order'),


]
