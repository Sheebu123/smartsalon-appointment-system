from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from payments.models import Payment

from .models import Appointment


class AppointmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer1',
            password='SmartSalon@123',
            role='CUSTOMER',
        )
        self.client.login(username='customer1', password='SmartSalon@123')

    def test_booking_creates_payment(self):
        response = self.client.post(
            reverse('appointments:create'),
            data={
                'service': 'HAIRCUT',
                'stylist_name': 'Riya',
                'appointment_datetime': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
                'notes': 'Weekend slot',
            },
        )
        self.assertEqual(response.status_code, 302)
        appointment = Appointment.objects.get(customer=self.user)
        self.assertTrue(Payment.objects.filter(appointment=appointment, status='PENDING').exists())

    def test_cannot_book_past_time(self):
        response = self.client.post(
            reverse('appointments:create'),
            data={
                'service': 'FACIAL',
                'stylist_name': 'Maya',
                'appointment_datetime': (timezone.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
                'notes': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'future date and time')
