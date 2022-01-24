from django_redis import get_redis_connection
from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework import status
from django.urls import reverse

from accounts.enums.enum_redis import RedisEnum
from accounts.models.user import User
from accounts.models.city import City
from accounts.models.grade import Grade
from django.core.cache import cache

SIGNUP_URL = reverse('signup')


class TestSignupView(APITestCase):
    fixtures = ['role.json']

    def setUp(self) -> None:
        self.phone_number = '09212587186'
        self.code = '1234'
        self.key = RedisEnum.tempCodeCategory.value + self.phone_number + ':' + self.code
        self.user = baker.make(User)
        self.city = baker.make(City)
        self.grade = baker.make(Grade)
        self.city.save()
        self.grade.save()
        self.user.set_password('1234')
        self.user.save()
        self.existed_user_code = '4321'
        self.existed_user_key = RedisEnum.tempCodeCategory.value + self.user.phone_number + ':' + self.existed_user_code
        cache.set(self.existed_user_key, True, timeout=60 * 2)

    def test_user_is_created(self):
        data = {'temp': self.code, 'password': '23572308', 'first_name': 'رت', 'last_name': 'تلر', 'city': self.city.id,
                'grades': self.grade.id}
        cache.set(self.key, True, timeout=60 * 2)
        response = self.client.post(SIGNUP_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(self.client.cookies['token'])
        self.assertFalse(len(cache.keys(RedisEnum.tempCodeCategory.value + "{0}:*".format(self.phone_number))))
        try:
            self.assertIsNotNone(User.objects.get(phone_number=self.phone_number))
        except:
            pass

    def test_user_is_existed(self):
        data = {'temp': self.existed_user_code, 'phone_number': self.user.phone_number,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name, 'city': 1, "grades": 1}
        response = self.client.post(SIGNUP_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(cache.keys(RedisEnum.tempCodeCategory.value + "{0}:*".format(self.phone_number[1:])))
        try:
            self.assertIsNotNone(User.objects.get(phone_number=self.phone_number))
        except:
            pass

    def test_data_when_name_is_null_or_not_valid(self):
        data = {'temp': self.code, 'password': '23572308', 'city': 1,
                'grades': 1}
        data.__setitem__('first_name', '')
        data.__setitem__('last_name', '')
        respone = self.client.post(SIGNUP_URL, data=data)
        self.assertEqual(respone.status_code, status.HTTP_400_BAD_REQUEST)

    def test_data_when_temp_code_is_not_existed(self):
        data = {'temp': '2345', 'password': '23572308', 'first_name': 'nima', 'last_name': 'parifard', 'city': 1,
                'grades': 1}
        response = self.client.post(SIGNUP_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        get_redis_connection("default").flushall()
