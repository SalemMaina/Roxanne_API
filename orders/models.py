from django.db import models
from stores.models import Store


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    customer_phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.store.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price


class Receipt(models.Model):
    class SmsStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="receipt")
    sms_status = models.CharField(
        max_length=10, choices=SmsStatus.choices, default=SmsStatus.PENDING
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    receipt_text = models.TextField()  # immutable snapshot, generated once at creation
    created_at = models.DateTimeField(auto_now_add=True)


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="idempotency_keys")
    request_hash = models.CharField(max_length=64)  # sha256 of the request body
    response_body = models.JSONField()
    status_code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("store", "key")