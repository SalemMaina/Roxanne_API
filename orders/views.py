from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination

from stores.permissions import HasStoreAPIKey
from .models import Order, Receipt
from .serializers import OrderSerializer, ReceiptSerializer
from .services import generate_receipt_text, send_receipt_sms


class OrderCursorPagination(CursorPagination):
    ordering = "-created_at"
    page_size = 20


class ReceiptCursorPagination(CursorPagination):
    ordering = "-created_at"
    page_size = 20


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/orders/       - paginated list of the authenticated store's orders
    POST /api/v1/orders/       - create a new order (+ items, + receipt, + SMS send)
    """
    serializer_class = OrderSerializer
    permission_classes = [HasStoreAPIKey]
    pagination_class = OrderCursorPagination

    def get_queryset(self):
        return Order.objects.filter(store=self.request.store).prefetch_related("items", "receipt")

    def perform_create(self, serializer):
        with transaction.atomic():
            order = serializer.save()
            receipt = Receipt.objects.create(
                order=order,
                receipt_text=generate_receipt_text(order),
            )
            send_receipt_sms(receipt)


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/orders/{id}/   - single order detail, scoped to own store
    """
    serializer_class = OrderSerializer
    permission_classes = [HasStoreAPIKey]

    def get_queryset(self):
        return Order.objects.filter(store=self.request.store).prefetch_related("items", "receipt")


class ReceiptListView(generics.ListAPIView):
    """
    GET /api/v1/receipts/      - paginated list of the authenticated store's receipts
    """
    serializer_class = ReceiptSerializer
    permission_classes = [HasStoreAPIKey]
    pagination_class = ReceiptCursorPagination

    def get_queryset(self):
        return Receipt.objects.filter(order__store=self.request.store).select_related("order")


class ReceiptDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/receipts/{id}/ - single receipt detail, scoped to own store
    """
    serializer_class = ReceiptSerializer
    permission_classes = [HasStoreAPIKey]

    def get_queryset(self):
        return Receipt.objects.filter(order__store=self.request.store).select_related("order")


class ReceiptResendView(APIView):
    """
    POST /api/v1/receipts/{id}/resend/ - re-trigger the SMS send for an
    existing receipt, scoped to the authenticated store's own receipts only.
    """
    permission_classes = [HasStoreAPIKey]

    def post(self, request, pk):
        receipt = get_object_or_404(
            Receipt.objects.select_related("order"),
            pk=pk,
            order__store=request.store,
        )

        send_receipt_sms(receipt)

        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data, status=status.HTTP_200_OK)