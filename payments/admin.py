from django.contrib import admin
from .models import MpesaPayment

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'phone_number', 'status', 'mpesa_receipt_number', 'created_at')
    list_filter = ('status',)
    search_fields = ('order__id', 'phone_number', 'mpesa_receipt_number', 'checkout_request_id')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  
            return [field.name for field in self.model._meta.fields]
        return []