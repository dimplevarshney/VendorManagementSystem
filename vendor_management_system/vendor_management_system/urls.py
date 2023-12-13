"""
URL configuration for vendor_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.urls import url
from vendor_profile_management import views as vendor_views
from purchase_order_tracking import views as po_views
from vendor_performance_evaluation import views as performance_views
urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('api/vendors/<str:vendor_code>/',vendor_views.VendorDetail.as_view(),name='vendor-details'),
    path('api/vendors/',vendor_views.VendorListView.as_view(),name='vendors-list'),
    path('api/purchase_orders/<str:po_number>/',po_views.PurchaseOrderDetail.as_view(),name='vendor-details'),
    path('api/purchase_orders/',po_views.PurchaseOrderListView.as_view(),name='vendors-list'),
    path('api/vendors/<str:vendor>/performance/',performance_views.VendorPerformanceDetails.as_view(),name='vendor-performance'),
]
