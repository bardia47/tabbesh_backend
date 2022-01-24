from django_redis import get_redis_connection
from rest_framework.test import APITestCase
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from accounts.enums.enum_redis import RedisEnum
from accounts.models.user import User
from model_bakery import baker
from freezegun import freeze_time
from datetime import datetime, timedelta

VALIDATE_TEMP_CODE_URL = reverse('validate-temp-code')


class TestTempCodeView(APITestCase):
    def setUp(self) -> 'it prepares temp code an test it':
        self.phone_number = '09212581786'
        self.code = '1234'
        self.key = 'TempCode' + ':' + self.phone_number + ':' + self.code
        cache.set(self.key, True, timeout=60 * 2)

    def test_code_is_correct(self):
        data = {'temp': self.code}
        response = self.client.post(VALIDATE_TEMP_CODE_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.keys(RedisEnum.tempCodeCategory.value + "{0}:*".format(self.phone_number[1:])))

    def test_code_is_not_existed(self):
        data = {'temp': '1244'}
        response = self.client.post(VALIDATE_TEMP_CODE_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        get_redis_connection("default").flushall()
