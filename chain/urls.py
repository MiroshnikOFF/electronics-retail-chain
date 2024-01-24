from django.urls import path

from chain.apps import TradeConfig
from chain.views import SupplierCreateAPIView, SupplierListAPIView, SupplierRetrieveAPIView, \
    SupplierUpdateAPIView, SupplierDestroyAPIView

app_name = TradeConfig.name

urlpatterns = [
    path('suppliers/create/', SupplierCreateAPIView.as_view(), name='supplier_create'),
    path('suppliers/', SupplierListAPIView.as_view(), name='suppliers'),
    path('suppliers/<int:pk>/', SupplierRetrieveAPIView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/update/', SupplierUpdateAPIView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', SupplierDestroyAPIView.as_view(), name='supplier_delete'),
]

