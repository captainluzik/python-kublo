from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.cabinet_api.serializers import UserSerializer

CustomUser = get_user_model()


class UserSerializerTestCase(TestCase):
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
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

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

