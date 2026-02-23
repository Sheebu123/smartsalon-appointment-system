from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    SERVICE_CHOICES = (
        ('HAIRCUT', 'Haircut'),
        ('FACIAL', 'Facial'),
        ('MANICURE', 'Manicure'),
        ('PEDICURE', 'Pedicure'),
    )
    STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    stylist_name = models.CharField(max_length=100)
    appointment_datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_datetime']
        constraints = [
            models.UniqueConstraint(
                fields=['stylist_name', 'appointment_datetime'],
                name='unique_stylist_appointment_slot',
            )
        ]

    def clean(self):
        if not self.appointment_datetime:
            return
        if self.appointment_datetime <= timezone.now():
            raise ValidationError('Appointment time must be in the future.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_service_price(self):
        prices = {
            'HAIRCUT': 20,
            'FACIAL': 35,
            'MANICURE': 25,
            'PEDICURE': 30,
        }
        return prices.get(self.service, 0)

    def __str__(self):
        return f'{self.customer.username} - {self.service} - {self.appointment_datetime:%Y-%m-%d %H:%M}'
