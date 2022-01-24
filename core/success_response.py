from rest_framework.response import Response
from rest_framework.exceptions import status
from core.serializer import SuccessSerializer


class SuccessResponse(Response):
    def __init__(self, message, status=status.HTTP_200_OK):
        super(SuccessResponse, self).__init__(SuccessSerializer(message).initial_data, status=status)
