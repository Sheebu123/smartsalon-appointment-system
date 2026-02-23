from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from appointments.models import Appointment

from .models import Payment


class PaymentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='payuser',
            password='SmartSalon@123',
            role='CUSTOMER',
        )
        self.client.login(username='payuser', password='SmartSalon@123')
        self.appointment = Appointment.objects.create(
            customer=self.user,
            service='MANICURE',
            stylist_name='Ana',
            appointment_datetime=timezone.now() + timedelta(days=1),
        )
        self.payment = Payment.objects.create(
            appointment=self.appointment,
            amount=25,
            status='PENDING',
        )

    def test_mark_paid(self):
        response = self.client.post(
            reverse('payments:mark_paid', kwargs={'payment_id': self.payment.id}),
            data={'method': 'CARD', 'transaction_reference': 'TXN12345'},
        )
        self.assertEqual(response.status_code, 302)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'PAID')
        self.assertEqual(self.payment.method, 'CARD')
