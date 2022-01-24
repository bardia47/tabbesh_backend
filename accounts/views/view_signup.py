from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from accounts.serializers.serializer_signup import *
from accounts.models import *
from rest_framework.response import Response
from accounts.views.view_signin import set_cookie_response
from django.shortcuts import get_object_or_404


class SignupView(ModelViewSet):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        request.data['phone_number'] = serializer.validated_data['phone_number']
        request.data['password'] = serializer.validated_data['password']
        # send token of user
        return set_cookie_response(request)
