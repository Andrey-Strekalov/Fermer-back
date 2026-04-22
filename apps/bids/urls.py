from django.urls import path

from .views import BidListCreateView


urlpatterns = [
    path('', BidListCreateView.as_view()),
]

