from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import CharField

from accounts.models.user import User
from core.validators import PHONE_NUMBER_REGEX_VALIDATOR
from core.utils.phonenumberutils import PhoneNumberUtils

class SendSmsSerializer(serializers.Serializer):
    phone_number = CharField(max_length=13,validators=[PHONE_NUMBER_REGEX_VALIDATOR])

    def validate_phone_number(self, value):
        # regex = ["^9\d{9}$", "^09\d{9}$", "^\\+989\d{9}$"]
        # f_1 = lambda value: value if (re.search(regex[0], value)) else False
        # f_2 = lambda value: value[1:] if re.search(regex[1],value) else False
        # f_3 = lambda value: value[2:] if re.search(regex[2], value) else False
        # value = reduce(lambda x, y: int(x) + int(y), {f_1(value), f_2(value), f_3(value)})
        value = PhoneNumberUtils.normilize_phone_number(value)
        return value


