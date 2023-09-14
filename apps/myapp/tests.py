from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from rest_framework import serializers, status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, PersonalCabinet
from .serializers import UserSerializer, AllInvestorsSerializer


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

        from datetime import datetime, timedelta
        one_year_term = datetime.now().date() + timedelta(days=365)

        self.data = {
            'email': self.email, 'first_name': 'Mr Solo',
            'last_name': 'Parker', 'partnership_code': 'PROMO123',
            'investment_sector': 'Test', 'deposit_term': one_year_term,
            'interest_rate': 1.342, 'password': self.password1,
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
        invalid_data['password2'] = "invalid password"
        serializer = UserSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.save()
            self.assertEqual(str(e.exception), "['Passwords must match!']")

    def test_invalid_email(self) -> None:
        invalid_data = self.data.copy()
        invalid_data['email'] = "invalid email"
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
        from datetime import datetime, timedelta
        one_year_term = datetime.now().date() + timedelta(days=365)

        self.data = {
            'email': 'test@gmail.com', 'first_name': 'Mr Solo',
            'last_name': 'Parker', 'partnership_code': 'PROMO123',
            'investment_sector': 'Test', 'deposit_term': one_year_term,
            'interest_rate': 1.342, 'password': 'Testpassword123',
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


class TestDecoratedTokenObtainPairView(APITestCase):
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


class TestPersonalCabinet(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="test@gmail.com",
            password="Testpassword123"
        )

        from datetime import datetime, timedelta
        one_year_term = datetime.now().date() + timedelta(days=365)

        self.data = {
            'user': self.user,
            'first_name': 'Tester',
            'last_name': 'Testenko',
            'partnership_code': 'PROMO123',
            'investment_sector': 'AI',
            'deposit_term': one_year_term,
            'interest_rate': 12.412
        }

        self.personal_cabinet = PersonalCabinet.objects.create(
            **self.data
        )

    def test_personal_cabinet_creation_valid_data(self) -> None:
        self.assertIsNotNone(self.personal_cabinet)
        self.assertEqual(self.personal_cabinet.user, self.user)
        self.assertEqual(self.personal_cabinet.first_name, self.data['first_name'])
        self.assertEqual(self.personal_cabinet.last_name, self.data['last_name'])
        self.assertEqual(self.personal_cabinet.partnership_code, self.data['partnership_code'])
        self.assertEqual(self.personal_cabinet.investment_sector, self.data['investment_sector'])
        self.assertEqual(self.personal_cabinet.deposit_term, self.data['deposit_term'])
        self.assertEqual(self.personal_cabinet.interest_rate, self.data['interest_rate'])

    def test_personal_cabinet_creation_invalid_data(self) -> None:
        invalid_data = self.data.copy()
        invalid_data['user'] = None

        with self.assertRaises(IntegrityError):
            personal_cabinet = PersonalCabinet.objects.create(
                **invalid_data
            )

            self.assertIsNone(personal_cabinet)
            self.assertEqual(PersonalCabinet.objects.all().count(), 0)

    def test_refferal_parthners_list(self) -> None:
        self.assertIs(type(self.personal_cabinet.referral_partners_list), list)

    def test_total_deposit_amount(self) -> None:
        self.assertIs(type(self.personal_cabinet.total_deposit_amount), float)

    def test_received_dividents_amount(self) -> None:
        self.assertIs(type(self.personal_cabinet.received_dividends_amount), float)

    def test_full_name(self) -> None:
        self.assertEqual(self.personal_cabinet.full_name, 'Tester Testenko')

    def test___str__(self) -> None:
        self.assertEqual(str(self.personal_cabinet), self.personal_cabinet.full_name)


class TestPersonalCabinetView(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email='testuser@gmail.com',
            password='testpassword')

        from datetime import datetime, timedelta
        self.one_year_term = datetime.now().date() + timedelta(days=365)

        self.cabinet = PersonalCabinet.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            partnership_code='12345BLA',
            investment_sector='AI',
            deposit_term=self.one_year_term,
            interest_rate=5.0,
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.url = '/api/personal-cabinet/'

    def test_authenticated_user_can_access_personal_cabinet(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "Full name": 'John Doe',
            "Partnership code": '12345BLA',
            "Investment sector": 'AI',
            "Deposit term": self.one_year_term,
            "Interest rate": 5.0,
            "Referral partners": [],
            "Deposit amount": 0.0,
            "Dividends amount": 0.0
        })

    def test_unauthenticated_user_cannot_access_personal_cabinet(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAllInvestorsView(APITestCase):
    def setUp(self) -> None:
        self.admin_user = CustomUser.objects.create_superuser(email='admin@gmail.com',
                                                              password='Adminpassword123')

        self.user = CustomUser.objects.create_user(email='testuser@gmail.com',
                                                   password='Testpassword123')

        from datetime import datetime, timedelta
        one_year_term = datetime.now().date() + timedelta(days=365)

        self.cabinet = PersonalCabinet.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            partnership_code='12345',
            investment_sector='AI',
            deposit_term=one_year_term,
            interest_rate=5.3
        )

        self.serializer = AllInvestorsSerializer(instance=PersonalCabinet.objects.all(),
                                                 many=True)

        self.admin_access_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.user_access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_admin_access(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}')

        response = self.client.get('/api/get-all-investors/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            f"{self.user}": {
                "ID": self.cabinet.id,
                "Full name": self.cabinet.full_name,
                "Partnership code": self.cabinet.partnership_code,
                "Investment sector": self.cabinet.investment_sector,
                "Deposit term": self.cabinet.deposit_term,
                "Interest rate": self.cabinet.interest_rate,
                "Referral partners": self.cabinet.referral_partners_list,
                "Deposit amount": self.cabinet.total_deposit_amount,
                "Dividends amount": self.cabinet.received_dividends_amount
            }
        })

    def test_non_admin_access(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')

        response = self.client.get('/api/get-all-investors/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"Access denied": "Only admin can access to this data"})


class TestCabinetUpdateView(APITestCase):
    def setUp(self) -> None:
        self.admin_user = CustomUser.objects.create_superuser(email='admin@gmail.com',
                                                              password='Adminpassword123')

        self.user = CustomUser.objects.create_user(email='testuser@gmail.com',
                                                   password='Testpassword123')

        from datetime import datetime, timedelta
        one_year_term = datetime.now().date() + timedelta(days=365)

        self.cabinet = PersonalCabinet.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            partnership_code='12345',
            investment_sector='AI',
            deposit_term=one_year_term,
            interest_rate=5.3
        )

        self.admin_access_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.user_access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_unauthenticated_user_update(self):
        from datetime import datetime, timedelta
        term = datetime.now().date() + timedelta(days=400)
        data = {
            'partnership_code': '456',
            'investment_sector': 'Technology',
            'deposit_term': term,
        }

        response = self.client.put(f"/api/cabinet-update/{self.cabinet.id}/",
                                   data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_access(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')

        from datetime import datetime, timedelta
        term = datetime.now().date() + timedelta(days=400)
        data = {
            'partnership_code': '456',
            'investment_sector': 'Technology',
            'deposit_term': term,
        }
        response = self.client.put(f"/api/cabinet-update/{self.cabinet.id}/",
                                   data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            "Access denied": "Only admin can access to this data"
        })

    def test_admin_access(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}')

        from datetime import datetime, timedelta
        term = datetime.now().date() + timedelta(days=400)
        data = {
            'partnership_code': '456PROMO',
            'investment_sector': 'Technology',
            'deposit_term': str(term),
        }

        response = self.client.put(f"/api/cabinet-update/{self.cabinet.id}/",
                                   data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

        updated_cabinet = PersonalCabinet.objects.get(pk=self.cabinet.pk)
        self.assertEqual(updated_cabinet.partnership_code, '456PROMO')
        self.assertEqual(updated_cabinet.investment_sector, 'Technology')
        self.assertEqual(str(updated_cabinet.deposit_term), str(term))
