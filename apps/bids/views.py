from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bid
from .pagination import BidPagination
from .serializers import BidCreateSerializer, BidListItemSerializer, BidSerializer


class BidListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = BidPagination
    queryset = Bid.objects.select_related('author').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BidCreateSerializer
        return BidListItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        bid_type = self.request.query_params.get('type')
        if bid_type is not None:
            if bid_type not in (Bid.TYPE_BUY, Bid.TYPE_SELL):
                raise ValidationError({'type': 'Invalid type. Allowed: buy, sell'})
            qs = qs.filter(type=bid_type)

        region = self.request.query_params.get('region')
        if region:
            qs = qs.filter(region__icontains=region.strip())

        author_id = self.request.query_params.get('author_id')
        if author_id and author_id.isdigit():
            qs = qs.filter(author_id=int(author_id))

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'author': request.user},
        )
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()

        return Response(
            {
                'success': True,
                'bid': BidSerializer(bid).data,
            },
            status=status.HTTP_201_CREATED,
        )

