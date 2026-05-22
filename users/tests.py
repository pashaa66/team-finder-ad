from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserModelTest(TestCase):
    def test_create_user_generates_avatar(self):
        user = User.objects.create_user(
            email='test1@test1.com',
            name='Test1',
            surname='Test1',
            password='12345',
        )
        self.assertTrue(bool(user.avatar))

    def test_phone_normalization(self):
        from users.forms import EditProfileForm

        user = User.objects.create_user(
            email='test2@test2.com',
            name='Test2',
            surname='Test2',
            password='12314',
        )
        form = EditProfileForm(
            {
                'name': 'Test2',
                'surname': 'Test2',
                'phone': '89001234567',
                'github_url': '',
                'about': '',
            },
            instance=user,
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['phone'], '+79001234567')


class RegisterViewTest(TestCase):
    def test_register(self):
        resp = self.client.post(
            reverse('users:register'),
            {
                'name': 'Test3',
                'surname': 'Test3',
                'email': 'test3@test3.com',
                'password': '12345',
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(email='test3@test3.com').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            email='test4@test4.com',
            name='Test4',
            surname='Test4',
            password='12345',
        )

    def test_login_success(self):
        resp = self.client.post(
            reverse('users:login'),
            {'email': 'test4@test4.com', 'password': '12345'},
        )
        self.assertEqual(resp.status_code, 302)

    def test_login_fail(self):
        resp = self.client.post(
            reverse('users:login'),
            {'email': 'test4@test4.com', 'password': '1234567'},
        )
        self.assertContains(resp, 'Неверный', status_code=200)
