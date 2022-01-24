from rest_framework import generics
from accounts.serializers.serializer_reset_password import ResetPasswordSerializer
from accounts.serializers.serializer_temp_code import TempCodeSerializer
from core.success_response import SuccessResponse
from core.serializer import SuccessSerializer


class TempCodeView(generics.GenericAPIView):
    serializer_class = TempCodeSerializer

    def post(self, request):
        serializer = TempCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return SuccessResponse('کد وارد شده صحیح است')
