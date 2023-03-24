
from rest_framework import serializers
from ..models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoiced_amount', 'invoice_date', 'paid', 'invoice_number']