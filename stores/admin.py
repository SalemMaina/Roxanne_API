from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import Store, StoreAPIKey


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "email")


@admin.register(StoreAPIKey)
class StoreAPIKeyAdmin(APIKeyModelAdmin):
    list_display = (*APIKeyModelAdmin.list_display, "store")
    search_fields = (*APIKeyModelAdmin.search_fields, "store__name")