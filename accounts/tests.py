from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='test'
            , email = 'test@email.com'
            , password = 'testpass123'
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username='test_superadmin'
            , email = 'test_superadmin@email.com'
            , password = 'testpass123'
        )
        self.assertEqual(admin.username, 'test_superadmin')
        self.assertEqual(admin.email, 'test_superadmin@email.com')
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


