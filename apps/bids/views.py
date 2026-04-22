from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BidCreateSerializer, BidSerializer


class BidListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BidCreateSerializer(
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

