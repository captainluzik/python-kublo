from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestCustomTokenObtainPairView(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model()

    def test_post_valid_data(self) -> None:
        user_data = {
            'email': "test@example.com",
            'password': "Testpassword123"
        }
        self.user.objects.create_user(**user_data)
        response = self.client.post('/api/token/', user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_post_invalid_data(self) -> None:
        user_data = {
            'email': "test@example.com",
            'password': "Testpassword123"
        }
        self.user.objects.create_user(**user_data)
        user_data['password'] = 'invalid_password'

        response = self.client.post('/api/token/', user_data, format='json')
        self.assertEqual(response.status_code, 401)
