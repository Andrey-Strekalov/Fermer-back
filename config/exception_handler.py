from django.http import Http404
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied, NotFound


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(exc, NotAuthenticated):
        response.data = {'success': False, 'detail': 'Учётные данные не предоставлены.'}
    elif isinstance(exc, AuthenticationFailed):
        response.data = {'success': False, 'detail': 'Неверный или истёкший токен.'}
    elif isinstance(exc, PermissionDenied):
        response.data = {'success': False, 'detail': 'Доступ запрещён.'}
    elif isinstance(exc, (Http404, NotFound)):
        response.data = {'success': False, 'detail': 'Объект не найден.'}

    return response
