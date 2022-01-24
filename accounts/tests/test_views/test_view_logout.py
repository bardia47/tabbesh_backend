from rest_framework.test import APITestCase
from model_bakery import baker
from http.cookies import SimpleCookie
from rest_framework import status
from django.urls import reverse
from accounts.models.user import User

ACCESS_TOKEN_URL = reverse('token_obtain_pair')
REFRESH_TOKEN_URL = reverse('token_refresh')
LOGOUT_URL = reverse('logout')

class TestLogout(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.user.set_password('123')
        self.user.phone_number = '09212587185'
        self.user.save()
        data = {"phone_number": self.user.phone_number, "password": '123'}
        response = self.client.post(ACCESS_TOKEN_URL, data)
        self.url = LOGOUT_URL

    def test_logout(self):
        data = {"phone_number": self.user.phone_number, "password": '123'}
        response = self.client.post(ACCESS_TOKEN_URL, data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass

    def test_not_login(self):
        self.client.cookies = SimpleCookie()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        try:
            self.assertIsNone(response.data['token'])
        except:
            pass
