from django.core.cache import cache
from rest_framework.viewsets import ModelViewSet

from accounts.enums.enum_redis import RedisEnum
from accounts.utils.temp_utils import ViewUtils
from accounts.serializers.serializer_reset_password import ResetPasswordSerializer
from django.shortcuts import get_object_or_404
from accounts.models import *
from accounts.views.view_signin import set_cookie_response

class ResetPasswordView(ModelViewSet):
    serializer_class = ResetPasswordSerializer

    def partial_update(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache_temp = cache.keys(RedisEnum.tempCodeCategory.value + "*:" + serializer.validated_data['temp'])[0]
        user_object = get_object_or_404(User, phone_number=ViewUtils.get_phone_number_from_temp_code(cache_temp))
        user_object.set_password(serializer.data['password'])
        user_object.save()
        cache.delete(cache_temp)
        # print(cache_temp)
        # cache.get(cache_temp)
        request.data['phone_number'] = user_object.phone_number
        # send token of user
        return set_cookie_response(request)
