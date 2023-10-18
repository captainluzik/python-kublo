from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.cabinet_api.serializers.user import UserSerializer
from apps.cabinet_api.models import PersonalAccount

CustomUser = get_user_model()


class UserSerializerCreateTestCase(TestCase):
    def test_create_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'pass1234',
            'password_confirm': 'pass1234',
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.password, user.check_password('pass1234'))

    def test_password_inequality(self):
        data = {
            'email': 'test@example.com',
            'password': 'pass1234',
            'password_confirm': 'pass12345',  # passwords doesn't match
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.create(data)

        # Check if the validation error message contains the expected text
        self.assertIn("Passwords do not match", str(context.exception))

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            email="test@example.com",
            password="pass1234"
        )

        data = {
            "email": "test@example.com",  # Same email as above
            "password": "pass12345",
            "password_confirm": "pass12345",
        }
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("email", context.exception.detail)
        # assert that ErrorDetail code is 'unique'
        self.assertEqual(
            context.exception.detail["email"][0].code, "unique"
        )


class UserSerializerUpdateTestCase(TestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(email="admintest@example.com", password="pass1234")
        self.regular_user = CustomUser.objects.create_user(email="regular@example.com", password="pass1234")

        self.client = APIClient()

    def test_admin_update_regular_user(self):
        # Test updating a regular user's account by an admin
        deposit_term = timezone.now().date()
        data = {
            "account": {
                "investment_sector": PersonalAccount.INVESTMENT_SECTOR_CHOICES[0][0],  # first investment sector choice
                "partner_code": "10charcode",
                "deposit_term_end": deposit_term,
            }
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f"/api/account/{self.regular_user.id}/", data=data, format='json')
        # response = self.client.put(reverse('account-update', args=[self.regular_user.id]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = CustomUser.objects.get(id=self.regular_user.id)
        self.assertEqual(updated_user.account.investment_sector, PersonalAccount.INVESTMENT_SECTOR_CHOICES[0][0])
        self.assertEqual(updated_user.account.partner_code, "10charcode")
        self.assertEqual(updated_user.account.deposit_term_end, deposit_term)

    def test_user_update(self):
        # Test that regular user can't update himself
        deposit_term = timezone.now().date()
        data = {
            "account": {
                "investment_sector": PersonalAccount.INVESTMENT_SECTOR_CHOICES[0][0],  # first investment sector choice
                "partner_code": "10charcode",
                "deposit_term_end": deposit_term,
            }
        }

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(f"/api/account/{self.regular_user.id}/", data=data, format='json')
        # response = self.client.put(reverse('account-update', args=[self.regular_user.id]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_term(self):
        # Test that you can't set deposit_term_end to the past
        deposit_term = timezone.now().date() - timezone.timedelta(days=30)
        data = {
            'account': {
                'deposit_term_end': deposit_term
            }
        }

        self.client.force_authenticate(self.admin_user)
        response = self.client.put(f"/api/account/{self.regular_user.id}/", data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid deposit term end date", str(response.content))

    def test_admin_update_invalid_field(self):
        # Test updating an invalid field
        deposit_term = timezone.now().date()
        data = {
            "account": {
                "investment_sector": "Invalid Sector",  # Invalid value
                "partner_code": "10charcode",
                "deposit_term_end": deposit_term,
            }
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f"/api/account/{self.regular_user.id}/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid choice.", str(response.content))
