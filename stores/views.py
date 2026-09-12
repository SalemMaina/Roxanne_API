from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import HasStoreAPIKey


class WhoAmIView(APIView):
    """
    Temporary diagnostic endpoint - confirms API key auth resolves
    to the correct store. Remove once orders app has real endpoints
    to test against.
    """
    permission_classes = [HasStoreAPIKey]

    def get(self, request):
        return Response({
            "store_id": request.store.id,
            "store_name": request.store.name,
            "is_active": request.store.is_active,
        })