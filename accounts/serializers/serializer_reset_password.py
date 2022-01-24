from rest_framework import serializers
from accounts.serializers.serializer_temp_code import TempCodeSerializer


class ResetPasswordSerializer(TempCodeSerializer):
    password = serializers.CharField(max_length=20)
    class Meta:
        fields = ('temp', 'password')



