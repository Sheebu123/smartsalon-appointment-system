from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'stylist_name', 'appointment_datetime', 'status')
    list_filter = ('service', 'status')
    search_fields = ('customer__username', 'stylist_name')
