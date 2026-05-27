from django.urls import path

from .views import ContactRequestDetailView, ContactRequestListCreateView, ContactRequestReadView

urlpatterns = [
    path('', ContactRequestListCreateView.as_view()),
    path('<int:pk>/', ContactRequestDetailView.as_view()),
    path('<int:pk>/read/', ContactRequestReadView.as_view()),
]
