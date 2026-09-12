from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import StoreAPIKey


class HasStoreAPIKey(BaseHasAPIKey):
    model = StoreAPIKey

    def has_permission(self, request, view):
        allowed = super().has_permission(request, view)
        if not allowed:
            return False

        # Attach the resolved store onto the request so views/querysets
        # can filter by it without re-parsing the key.
        key = self.get_key(request)
        api_key = StoreAPIKey.objects.get_from_key(key)
        request.store = api_key.store
        return request.store.is_active