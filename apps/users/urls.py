from django.urls import path
from . import views
from .views import RequestCodeView, ConfirmCodeView

urlpatterns = [
    path('request-code/', views.RequestCodeView.as_view()),
    path('confirm-code/', views.ConfirmCodeView.as_view()),
]
