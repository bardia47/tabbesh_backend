from django.core.cache import cache
from rest_framework import serializers

from accounts.utils.temp_utils import SerializerUtils


class TempCodeSerializer(serializers.Serializer):
    temp = serializers.CharField(max_length=4, write_only=True, required=True)

    class Meta:
        fields = ('temp')

    def validate_temp(self, value):
        cache.expire(SerializerUtils.check_expire(value), 15 * 60)
        return value
