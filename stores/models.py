from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


class Store(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)  # store's own phone/contact
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StoreAPIKey(AbstractAPIKey):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="api_keys"
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Store API key"
        verbose_name_plural = "Store API keys"