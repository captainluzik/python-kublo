import json

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestRegistration(APITestCase):
    def test_valid_registration(self):
        registration_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("register"), data=registration_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.assertIn("access", response_data) and self.assertIn("refresh", response_data)

    def test_invalid_email(self):
        registration_data_email_invalid = {
            "email": "testexample.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("register"), data=registration_data_email_invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)

    def test_invalid_passwords(self):
        registration_data_passwords_invalid = {
            "email": "test@example.com",
            "password": "testpassword",
            "password2": "testpassword1234",
        }

        response = self.client.post(reverse("register"), data=registration_data_passwords_invalid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("password2", response_data)
