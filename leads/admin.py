from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    fields = ['invoiced_amount', 'paid']
    # Meerdere invoices toevoegen lukt niet wegens issue met prefixed_invoice
    
class Invoiced_over_1000(admin.SimpleListFilter):
    # Hier een filter toevoegen voor bedragen > 1000
    title = ('Invoiced over 1000')
    parameter_name = 'amount'
    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('1000', 'billed 1000 or more')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is not None:
            return queryset.filter(user_invoice__invoiced_amount__gte=self.value()).distinct()
        else: return queryset
        
class Unpaid(admin.SimpleListFilter):
    # Hier een filter toevoegen voor users die onbetaalde invoice hebben
    title = ('Users with Unpaid Invoices')
    parameter_name = 'paid'
    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('unpaid_users', 'Unpaid Invoice Users')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is not None:
            return queryset.filter(user_invoice__paid=False).distinct()
        else: return queryset
    
        
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'company_name', 'country', 'invoice_currency')
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'country', 'invoice_currency', 'user_invoices_link')
    list_filter = ('company_name', 'country', Invoiced_over_1000, Unpaid)
    
    inlines = [InvoiceInline]
    
    def user_invoices_link(self, obj):
        url = "../invoice/?q=" + obj.first_name
        link = f'<a href="{url}">Invoices</a>'
        return mark_safe(link)
    
    
    
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fields = ['user','invoiced_amount', 'paid']
    list_filter = ['user__first_name','invoiced_amount', 'invoice_date', 'paid', 'invoice_number']
    list_display = ['user','invoiced_amount', 'invoice_date', 'paid', 'invoice_number']
    search_fields = ['user__first_name']