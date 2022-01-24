from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.utils.phonenumberutils import PhoneNumberUtils


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['phone_number']= PhoneNumberUtils.normilize_phone_number(attrs['phone_number'])
        return super().validate(attrs)

