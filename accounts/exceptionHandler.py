from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import render, redirect
from rest_framework.response import Response

def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
            if context['request'].accepted_renderer.format == 'html':
                return redirect('/signin/?next='+context['request'].path)

    return response