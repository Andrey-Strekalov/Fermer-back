from django.urls import path
from .views import (
    RequestCodeView, ConfirmCodeView, CurrentUserView,
    RefreshAccessTokenView, LogoutView,
)

urlpatterns = [
    path('request-code/', RequestCodeView.as_view()),
    path('confirm-code/', ConfirmCodeView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('refresh-token/', RefreshAccessTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
]
