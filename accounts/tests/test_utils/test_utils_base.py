from django_redis import get_redis_connection
from rest_framework.test import APITestCase
from accounts.enums.enum_redis import RedisEnum
from django.core.cache import cache


class TestBaseUtils(APITestCase):

    def setUp(self) -> None:
        self.code = '4321'
        self.wrong_code = '1234'
        self.phone_number = "09111111111"
        self.key = RedisEnum.tempCodeCategory.value +self.phone_number  + ':' + self.code
        cache.set(self.key, True, timeout=60 * 2)

    def tearDown(self):
        get_redis_connection("default").flushall()
