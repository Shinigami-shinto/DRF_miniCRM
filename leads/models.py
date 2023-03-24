from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    company_name = models.CharField(max_length=30)
    country = models.CharField(max_length=10)  # There is probably a better model out there
    invoice_currency = models.CharField(max_length=10)  # There is probably a better model out there
    def __str__(self):
        return self.first_name
    
    
class Invoice(models.Model):
    user = models.ForeignKey(User, db_column="user", on_delete=models.PROTECT, related_name='user_invoice')
    invoiced_amount = models.IntegerField()
    invoice_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=9, blank=True, unique=True, default='')
    
    @property
    def prefixed_invoice(self):
          # OTA prefix
        formatted_string = f"OTA-{self.pk:05d}"
        self.invoice_number = formatted_string
        self.save()
        return formatted_string

              
    def __str__(self):
        return self.prefixed_invoice
    