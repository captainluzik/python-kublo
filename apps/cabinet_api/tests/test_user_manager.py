from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        email = 'test123@example.com'
        password = 'test1234'

        user = CustomUser.objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_super_user(self):
        email = 'superuser@example.com'
        password = 'superpassword'

        superuser = CustomUser.objects.create_superuser(email, password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
