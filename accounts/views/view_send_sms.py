from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from accounts.enums.enum_redis import RedisEnum
from accounts.utils.temp_utils import ViewUtils
from accounts.models import User
from accounts.serializers.serializer_send_sms import SendSmsSerializer
from rest_framework import generics
from core.webservices.sms_sender import SmsWebServices
from accounts.enums.enum_sms import SmsEnum
from core.success_response import SuccessResponse
from core.exceptions import BadRequestError, ServerError


class SendSmsView(generics.GenericAPIView):
    serializer_class = SendSmsSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name='forgetPassword', in_=openapi.IN_QUERY, required=True, type=openapi.TYPE_BOOLEAN,
                          description='for different of forgetPassword and Signup')
    ]
    )
    def post(self, request):
        method = request.GET.get('forgetPassword')
        if method and method == 'true':
            return send_sms(request, True)
        return send_sms(request, False)


def send_sms(request, is_user_existed):
    serializer = SendSmsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data['phone_number']
    is_user_have_this_phone = User.objects.filter(phone_number=phone_number).first()
    if is_user_have_this_phone and not is_user_existed:
        raise BadRequestError("we have this phone number")
    elif is_user_existed and not is_user_have_this_phone:
        raise BadRequestError("we don't have this phone number")
    new_temp_code = ViewUtils.create_new_temp_code()
    is_created_cache = ViewUtils.create_cache_if_not_exists(RedisEnum.tempCodeCategory.value, phone_number, new_temp_code,
                                                            60 * 2)
    if not is_created_cache:
        raise BadRequestError("sms have sent you")
    sendSms = SmsWebServices.send_sms(phone_number, new_temp_code, SmsEnum.signupBodyId.value)
    if sendSms is not None:
        raise ServerError(sendSms)
    return SuccessResponse(('ارسال با موفقیت انجام شد'))
