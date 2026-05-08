from django.urls import path

from .views import BidListCreateView, BidArchiveView, BidUnarchiveView


urlpatterns = [
    path('', BidListCreateView.as_view()),
    path('<int:pk>/archive/', BidArchiveView.as_view()),
    path('<int:pk>/unarchive/', BidUnarchiveView.as_view()),
]

