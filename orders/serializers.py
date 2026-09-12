from rest_framework import serializers
from .models import Order, OrderItem, Receipt


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity', 'unit_price', 'line_total']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'sms_status', 'sent_at', 'receipt_text']


class OrderSerializer(serializers.ModelSerializer):
    """
    Used for both reading (list/detail) and writing (create).
    'store' is deliberately excluded from writable fields — it's set
    in the view from request.store, never trusted from client input.
    'total_amount' is read-only — computed server-side in the view
    from the submitted items, never trusted from client input.
    """
    items = OrderItemSerializer(many=True)
    receipt = ReceiptSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_phone', 'total_amount', 'created_at', 'items', 'receipt']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        store = self.context['request'].store

        total_amount = sum(
            item['quantity'] * item['unit_price'] for item in items_data
        )

        order = Order.objects.create(
            store=store,
            total_amount=total_amount,
            **validated_data,
        )

        OrderItem.objects.bulk_create([
            OrderItem(order=order, **item_data) for item_data in items_data
        ])

        return order