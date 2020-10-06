from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import redirect


def api_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        if context['request'].accepted_renderer.format == 'html':
            return redirect('/signin/?next=' + context['request'].get_full_path())
    response = exception_handler(exc, context)
    return response
