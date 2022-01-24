from rest_framework import serializers

from accounts.enums.enum_redis import RedisEnum
from accounts.utils.temp_utils import SerializerUtils
from accounts.models.user import User
from django.core.cache import cache
from core.exceptions import BadRequestError


class SignupSerializer(serializers.ModelSerializer):
    temp = serializers.CharField(max_length=4, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('temp', 'password', 'first_name', 'last_name', 'city', 'grades')

    def validate_temp(self, value):
        SerializerUtils.check_expire(value)
        return value

    def validate(self, data):
        data = super(SignupSerializer, self).validate(data)  # calling default validation
        cache_temp = cache.keys(RedisEnum.tempCodeCategory.value + "*:" + data['temp'])[0]
        phone_number = cache_temp[cache_temp.find(':') + 1:cache_temp.rfind(':')]
        data['phone_number'] = phone_number
        if User.objects.filter(phone_number=data['phone_number']).first():
            raise BadRequestError("duplicate phone number")
        cache.delete(cache_temp)
        return data

    def create(self, validated_data):
        data = {**validated_data}
        data.pop('temp', None)
        return User.objects.create_user(**data)
