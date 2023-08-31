"""
Tests for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:login')


def create_user(**params):
    """creates a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Represents tests for public deals with user"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """tests successful creating user"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """tests if it returns error while creating
        user with existing email"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """tests if it returns error if password less then 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pa',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """tests generating token for valid credentials"""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_wrong_password(self):
        """tests generating token with wrong password"""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'correct_password'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_wrong_email(self):
        """tests generating token with wrong email"""
        user_details = {
            'name': 'Test Name',
            'email': 'correct@example.com',
            'password': 'testpass123'
        }
        create_user(**user_details)

        payload = {
            'email': 'wrong@example.com',
            'password': 'testpass123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('user', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """tests generating token with blank password"""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('user', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
