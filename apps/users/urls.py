from django.urls import path
from . import views

urlpatterns = [
    path('request-code/', views.RequestCodeView.as_view()),
    path('verify-code/', views.VerifyCodeView.as_view()),
]
