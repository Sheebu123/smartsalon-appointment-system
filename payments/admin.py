from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'amount', 'method', 'status', 'paid_at')
    list_filter = ('status', 'method')
    search_fields = ('appointment__customer__username', 'transaction_reference')
