from django.urls import path
from . import views
from .views import RequestCodeView, ConfirmCodeView, CurrentUserView, RefreshAccessTokenView

urlpatterns = [
    path('request-code/', RequestCodeView.as_view()),
    path('confirm-code/', ConfirmCodeView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('refresh-token/', RefreshAccessTokenView.as_view()),
]
