from django.urls import path
from .views import OrderListCreateView, OrderDetailView, ReceiptListView, ReceiptDetailView, ReceiptResendView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("receipts/", ReceiptListView.as_view(), name="receipt-list"),
    path("receipts/<int:pk>/resend/", ReceiptResendView.as_view(), name="receipt-resend"),
    path("receipts/<int:pk>/", ReceiptDetailView.as_view(), name="receipt-detail"),
]