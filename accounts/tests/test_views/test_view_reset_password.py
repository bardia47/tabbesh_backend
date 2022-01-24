from django_redis import get_redis_connection
from rest_framework.test import APITestCase
from model_bakery import baker
from http.cookies import SimpleCookie
from rest_framework import status
from django.urls import reverse
from accounts.models.user import User
from django.core.cache import cache

RESETPASSWORD_URL = reverse('reset_password')


class TestResetPasswordView(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make('accounts.User', phone_number='09212587185')
        self.user.set_password('1234')
        self.user.save()
        self.code = '1234'
        self.key = 'TempCode' + ':' + self.user.phone_number + ':' + self.code
        self.phone_number_user_is_not_existed = '09212587186'
        self.keys_user_is_not_existed = 'TempCode' + ':' + self.phone_number_user_is_not_existed + ':' + '4321'
        cache.set(self.keys_user_is_not_existed, True, timeout=60 * 2)

    def test_password_is_changed(self):
        cache.set(self.key, True, timeout=60 * 2)
        data = {'temp': self.code, 'password': '23572308'}
        response = self.client.patch(RESETPASSWORD_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            self.assertIsNotNone(User.objects.filter(phone_number=self.user.phone_number).first())
        except:
            pass

    def test_reset_password_when_user_is_not_existed(self):
        data = {'temp': '4321', 'password': '23572308'}
        response = self.client.patch(RESETPASSWORD_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        try:
            self.assertIsNotNone(User.objects.filter(phone_number=self.phone_number_user_is_not_existed).first())
        except:
            pass

    def test_temp_code_is_not_existed(self):
        data = {'temp': '1345', 'password': '23572308'}
        response = self.client.patch(RESETPASSWORD_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        get_redis_connection("default").flushall()
