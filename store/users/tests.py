from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User

# Create your tests here.

class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'yevgenii', 'last_name': 'lebediev',
            'username': 'aboba', 'email': 'aboba@gmail.com',
            'password1': 'Abobapassword10190', 'password2': 'Abobapassword10190',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        responce = self.client.get(self.path)

        self.assertEqual(responce.status_code, HTTPStatus.OK)
        self.assertEqual(responce.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(responce, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        responce = self.client.post(self.path, self.data)
        self.assertEqual(responce.status_code, HTTPStatus.FOUND)
        self.assertRedirects(responce, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username=self.data['username']
        user=User.objects.create(username=username)
        responce = self.client.post(self.path, self.data)

        self.assertEqual(responce.status_code,HTTPStatus.OK)
        self.assertContains(responce,'Пользователь с таким именем уже существует.',html=True)
