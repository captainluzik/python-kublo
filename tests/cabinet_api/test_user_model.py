from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestUserModel(APITestCase):
    user_model = get_user_model()

    def test_custom_user_creation(self):
        user_data = {
            "email": "test123@example.com",
            "password": "testpassword",
        }
        user = self.user_model.objects.create_user(**user_data)
        self.assertNotEqual(user_data["password"], user.password)
        self.assertEqual(user.email, user.username)

    def test_superuser_creation(self):
        user_data = {
            "email": "test123super@example.com",
            "password": "testpassword",
        }
        user = self.user_model.objects.create_superuser(**user_data)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
