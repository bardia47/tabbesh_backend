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

SMSSEND_URL = reverse('send_sms')


class TestSendSmsView(APITestCase):
    def setUp(self) -> 'prepare phone number foe testing sms':
        self.phone_number = '09111111111'
        self.user = baker.make('accounts.User')
        self.user.set_password('123')
        self.user.save()
        self.exist_phone_number = '09212587187'
        self.keys = 'TempCode' + ':' + self.exist_phone_number + ':' + "1234"
        cache.set(self.keys, True, timeout=60 * 2)

    # def test_sms_send(self):
    #     data = {'phone_number': self.phone_number}
    #     response = self.client.post(SMSSEND_URL, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsNotNone(cache.keys("TempCode:{0}:*".format(self.phone_number)))
    #     try:
    #         self.assertIsNone(User.objects.filter(phone_number=self.phone_number).first())
    #     except:
    #         pass

    def test_user_is_existed(self):
        data = {'phone_number': self.user.phone_number}
        response = self.client.post(SMSSEND_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(cache.keys(RedisEnum.tempCodeCategory.value + "{0}:*".format(self.user.phone_number)))
        try:
            self.assertIsNotNone(User.objects.filter(phone_number=self.user.phone_number))
        except:
            pass

    def test_temp_code_is_existed(self):
        data = {'phone_number': self.exist_phone_number}
        respone = self.client.post(SMSSEND_URL, data=data)
        self.assertEqual(respone.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(cache.keys(RedisEnum.tempCodeCategory.value + "{0}:*".format(self.exist_phone_number)))
        try:
            self.assertIsNone(User.objects.filter(phone_number=self.phone_number).first())
        except:
            pass

    def test_number_is_not_valid(self):
        data = {'phone_number': '0921'}
        response = self.client.post(SMSSEND_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_code_is_expired(self):
    #     data = {'phone_number': '09212587185'}
    #     response = self.client.post(SMSSEND_URL, data=data)
    #     initial_datetime = datetime.now()
    #     with freeze_time(initial_datetime) as frozen_time:
    #         frozen_time.tick()
    #         initial_datetime += timedelta(minutes=3)
    #         self.assertIsNone(cache.keys("TempCode:{0}:*".format(self.phone_number)))

    def tearDown(self):
        get_redis_connection("default").flushall()
