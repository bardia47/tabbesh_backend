from random import randint
from accounts.enums.enum_redis import RedisEnum
from django.core.cache import cache
from rest_framework.exceptions import ValidationError


class SerializerUtils:
    @staticmethod
    def check_expire(value):
        cache_temp = cache.keys(RedisEnum.tempCodeCategory.value + "*:" + value)
        if not cache_temp:
            raise ValidationError("کد شما منقضی شده است. لطفا دوباره ثبت نام کنید.")
        return cache_temp


class ViewUtils:
    @staticmethod
    def get_phone_number_from_temp_code(cache_temp):
        return cache_temp[cache_temp.find(':') + 1:cache_temp.rfind(':')]

    @staticmethod
    def create_new_temp_code():
        new_temp_code = randint(1000, 9999).__str__()
        while True:
            if not cache.keys(RedisEnum.tempCodeCategory.value + "*:" + new_temp_code):
                break
            new_temp_code = randint(1000, 9999).__str__()
        return new_temp_code

    @staticmethod
    def create_cache_if_not_exists(category, first_key, second_key, expire_date):
        key = category + first_key + ":"
        if cache.keys(key + "*"):
            return False
        key += second_key
        cache.set(key, True, timeout=expire_date)
        return True
