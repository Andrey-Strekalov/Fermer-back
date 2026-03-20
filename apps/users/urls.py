from django.urls import path
from . import views
from .views import RequestCodeView, ConfirmCodeView, CurrentUserView


urlpatterns = [
    path('request-code/', RequestCodeView.as_view()),
    path('confirm-code/', ConfirmCodeView.as_view()),
    path('me/', CurrentUserView.as_view()),
]
