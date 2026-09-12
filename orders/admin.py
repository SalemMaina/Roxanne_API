from django.contrib import admin
from .models import Order, OrderItem, Receipt, IdempotencyKey


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class ReceiptInline(admin.StackedInline):
    model = Receipt
    extra = 0
    readonly_fields = ("sms_status", "sent_at", "receipt_text")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "customer_phone", "total_amount", "created_at")
    list_filter = ("store",)
    search_fields = ("customer_phone",)
    inlines = [OrderItemInline, ReceiptInline]


@admin.register(IdempotencyKey)
class IdempotencyKeyAdmin(admin.ModelAdmin):
    list_display = ("key", "store", "status_code", "created_at")
    list_filter = ("store", "status_code")
    readonly_fields = [f.name for f in IdempotencyKey._meta.fields]