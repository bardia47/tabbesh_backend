from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework import status
from django.urls import reverse

ACESS_TOKEN_URL = reverse('token_obtain_pair')
REFRESH_TOKEN_URL = reverse('token_refresh')


class TokenObtainPairView(APITestCase):
    def setUp(self) -> 'set up model baker for login user':
        self.phone_number = '09212587186'
        self.user = baker.make('accounts.User')
        self.user.set_password('23572308')
        self.user.phone_number = self.phone_number
        self.user.save()
        self.url = ACESS_TOKEN_URL

    def test_token_when_user_is_existed(self):
        data = {"phone_number": self.phone_number, "password": '23572308'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])
        self.assertTrue(self.client.cookies['token']['httponly'])

    def test_token_when_phone_number_is_not_correct(self):
        data = {"phone_number": "09212587180", "password": '23572308'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_token_when_password_is_not_correct(self):
        data = {"phone_number": self.phone_number, "password": "123"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
