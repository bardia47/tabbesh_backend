from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, NotFound
from django.shortcuts import redirect


def api_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        if context['request'].accepted_renderer.format == 'html':
            return redirect('/signin/?next=' + context['request'].get_full_path())

    if isinstance(exc, Http404):
        if context['request'].accepted_renderer.format == 'html':
            return redirect('page-not-found')

    if isinstance(exc, NotFound):
        if context['request'].accepted_renderer.format == 'html':
            return redirect('page-not-found')

    response = exception_handler(exc, context)
    return response
