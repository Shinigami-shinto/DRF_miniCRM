from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Invoice
from .serializers.invoices import InvoiceSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.throttling import SimpleRateThrottle

class UserInvoiceThrottle(SimpleRateThrottle):
    rate = '10/minute'
    scope_attr = 'user'

    def get_cache_key(self, request, view):
        # Use the IP address of the user as the cache key
        return self.get_ident(request)


class UnpaidInvoices(APIView):
    serializer_class = InvoiceSerializer
    throttle_classes = [UserInvoiceThrottle]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        invoices = Invoice.objects.filter(user=user, paid=False)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
