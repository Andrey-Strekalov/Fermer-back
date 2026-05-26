from django.urls import path

from .views import (
    BidArchiveView,
    BidListCreateView,
    BidUnarchiveView,
    BidUpdateView,
)


urlpatterns = [
    path('', BidListCreateView.as_view()),
    path('<int:pk>/archive/', BidArchiveView.as_view()),
    path('<int:pk>/unarchive/', BidUnarchiveView.as_view()),
    path('<int:pk>/', BidUpdateView.as_view()),
]

