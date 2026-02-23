from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountTests(TestCase):
    def test_register_creates_customer_user(self):
        response = self.client.post(
            reverse('accounts:register'),
            data={
                'username': 'john',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password1': 'SmartSalon@123',
                'password2': 'SmartSalon@123',
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='john')
        self.assertEqual(user.role, 'CUSTOMER')
