from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class LogoutView(generics.GenericAPIView):
    """
        token cookie will be deleted when user logs out.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request):
        response = Response("logout user")
        response.delete_cookie('token')
        return response
