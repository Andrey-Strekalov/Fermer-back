from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q

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

        status_filter = self.request.query_params.get('status')
        if status_filter is None or status_filter == 'active':
            qs = qs.filter(is_archived=False)
        elif status_filter == 'archived':
            qs = qs.filter(is_archived=True, author=self.request.user)
        elif status_filter == 'all':
            qs = qs.filter(
                Q(is_archived=False) | Q(is_archived=True, author=self.request.user)
            )
        else:
            raise ValidationError({'status': 'Некорректный статус. Допустимые значения: active, archived, all'})

        bid_type = self.request.query_params.get('type')
        if bid_type is not None:
            if bid_type not in (Bid.TYPE_BUY, Bid.TYPE_SELL):
                raise ValidationError({'type': 'Некорректный тип. Допустимые значения: buy, sell'})
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


class BidArchiveView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk: int):
        try:
            bid = Bid.objects.select_related('author').get(pk=pk)
        except Bid.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Заявка не найдена'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if bid.author_id != request.user.id:
            return Response(
                {'success': False, 'detail': 'Недостаточно прав для архивирования заявки'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not bid.is_archived:
            bid.is_archived = True
            bid.save(update_fields=['is_archived'])

        return Response(
            {'success': True, 'bid': BidSerializer(bid).data},
            status=status.HTTP_200_OK,
        )


class BidUnarchiveView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk: int):
        try:
            bid = Bid.objects.select_related('author').get(pk=pk)
        except Bid.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Заявка не найдена'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if bid.author_id != request.user.id:
            return Response(
                {'success': False, 'detail': 'Недостаточно прав для восстановления заявки'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if bid.is_archived:
            bid.is_archived = False
            bid.save(update_fields=['is_archived'])

        return Response(
            {'success': True, 'bid': BidSerializer(bid).data},
            status=status.HTTP_200_OK,
        )

