from django.urls import path
from .views import UnpaidInvoices
app_name = "leads"

urlpatterns = [
    path('unpaid-invoices/<int:user_id>/', UnpaidInvoices.as_view(), name='unpaid_invoices')    
]