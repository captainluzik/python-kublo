from pprint import pprint
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import serializers, status
from rest_framework.test import APITestCase
from .models import CustomUser
from .serializers import UserSerializer


class TestCustomUserManager(TestCase):
    def setUp(self) -> None:
        self.manager = CustomUser.objects

    def test_create_user_valid_data(self) -> None:
        email = "test@gmail.com"
        password = "Testpassword123"

        user = self.manager.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)

    def test_create_user_invalid_email(self) -> None:
        email = "test"
        password = "Testpassword123"
        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                email=email,
                password=password
            )

        self.assertEqual(str(e.exception), "['Invalid email format!']")

    def test_create_user_no_email(self) -> None:
        password = "Testpassword123"

        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                password=password
            )

        self.assertEqual(str(e.exception), "['The Email field is required!']")

    def test_create_user_no_password(self) -> None:
        email = "test@gmail.com"

        with self.assertRaises(ValidationError) as e:
            self.manager.create_user(
                email=email,
            )
        self.assertEqual(str(e.exception), "['The Password field is required!']")

    def test_create_superuser_valid_data(self) -> None:
        email = "test@gmail.com"
        password = "Testpassword123"

        user = self.manager.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)

    def test_create_superuser_invalid_email(self) -> None:
        email = "test"
        password = "Testpassword123"
        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                email=email,
                password=password
            )

        self.assertEqual(str(e.exception), "['Invalid email format!']")

    def test_create_superuser_no_email(self) -> None:
        password = "Testpassword123"

        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                password=password
            )

        self.assertEqual(str(e.exception), "['The Email field is required!']")

    def test_create_superuser_no_password(self) -> None:
        email = "test@gmail.com"

        with self.assertRaises(ValidationError) as e:
            self.manager.create_superuser(
                email=email,
            )
        self.assertEqual(str(e.exception), "['The Password field is required!']")


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="test@gmail.com",
            password="Testpassword123"
        )
        self.superuser = CustomUser.objects.create_superuser(
            email="test1@gmail.com",
            password="Testpassword123"
        )

    def test___str__(self) -> None:
        self.assertEqual(str(self.user), self.user.email)

    def test_user_is_staff(self) -> None:
        self.assertFalse(self.user.is_admin)

    def test_superuser_is_staff(self) -> None:
        self.assertTrue(self.superuser.is_admin)

    def test_create_user(self) -> None:
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_create_superuser(self) -> None:
        self.assertTrue(isinstance(self.superuser, CustomUser))
        self.assertEqual(self.superuser.email, 'test1@gmail.com')
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_admin)


class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        self.email = 'test@gmail.com'
        self.password1 = self.password2 = 'Testpassword123'

        self.data = {
            'email': self.email,
            'password': self.password1,
            'password2': self.password2
        }

    def test_valid_user_data(self) -> None:
        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_user_data(self) -> None:
        serializer = UserSerializer(data={'email': "test", 'password': "test"})
        with self.assertRaises(serializers.ValidationError) as e:
            self.assertFalse(serializer.is_valid())
            self.assertEqual(str(e.exception), "['Current email is invalid or already taken!']")
        self.assertIn('email', serializer.errors)

    def test_passwords_not_matching(self) -> None:
        invalid_data = self.data.copy()
        invalid_data['password2'] = "sdfssgsgdf"
        serializer = UserSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.save()
            self.assertEqual(str(e.exception), "['Passwords must match!']")

    def test_invalid_email(self) -> None:
        invalid_data = self.data.copy()
        invalid_data['email'] = "sdfssgsgdf"
        serializer = UserSerializer(data=invalid_data)
        with self.assertRaises(serializers.ValidationError) as e:
            self.assertFalse(serializer.is_valid())
            self.assertEqual(str(e.exception), "['Current email is invalid or already taken!']")
        self.assertIn('email', serializer.errors)

    def test_duplicate_email(self) -> None:
        CustomUser.objects.create_user(email='test@gmail.com', password='Testpassword123')

        serializer = UserSerializer(data=self.data)
        with self.assertRaises(serializers.ValidationError) as e:
            self.assertFalse(serializer.is_valid())
            self.assertEqual(str(e.exception), "['Current email is invalid or already taken!']")
        self.assertIn('email', serializer.errors)

    def test_save(self) -> None:
        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.data['email'])


class TestUserCreationView(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'test@gmail.com',
            'password': 'Testpassword123',
            'password2': 'Testpassword123'
        }

    def test_create_user(self) -> None:
        response = self.client.post('/api/create-user/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

        user = CustomUser.objects.get()
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.check_password(self.data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)

    def test_create_user_invalid_data(self) -> None:
        invalid_data = self.data.copy()
        invalid_data['email'] = "invalid_email"
        response = self.client.post('/api/create-user/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
