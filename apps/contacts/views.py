from django.db import IntegrityError
from django.db.models import Q

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bids.models import Bid
from apps.notifications.models import Notification
from .models import ContactRequest
from .serializers import ContactRequestCreateSerializer, ContactRequestSerializer


class ContactRequestListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        direction = request.query_params.get('direction')
        is_read = request.query_params.get('is_read')

        if direction == 'incoming':
            qs = ContactRequest.objects.filter(receiver=request.user)
        elif direction == 'outgoing':
            qs = ContactRequest.objects.filter(sender=request.user)
        else:
            qs = ContactRequest.objects.filter(
                Q(receiver=request.user) | Q(sender=request.user)
            )

        if is_read == 'false':
            qs = qs.filter(is_read=False)

        qs = qs.select_related('bid', 'sender', 'receiver').order_by('-created_at')
        serializer = ContactRequestSerializer(qs, many=True)
        return Response({'success': True, 'contact_requests': serializer.data})

    def post(self, request):
        serializer = ContactRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bid_id = serializer.validated_data['bid_id']
        comment = serializer.validated_data['comment']

        try:
            bid = Bid.objects.get(pk=bid_id)
        except Bid.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Заявка не найдена'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if bid.is_archived:
            return Response(
                {'success': False, 'detail': 'Нельзя отправить запрос по архивной заявке'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user == bid.author:
            return Response(
                {'success': False, 'detail': 'Нельзя отправить запрос по своей заявке'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            company_name = request.user.requisites.company_name
        except Exception:
            company_name = ''

        try:
            contact_request = ContactRequest.objects.create(
                bid=bid,
                sender=request.user,
                receiver=bid.author,
                comment=comment,
                sender_phone_snapshot=request.user.phone_number,
                sender_organization_snapshot=company_name,
            )
        except IntegrityError:
            return Response(
                {'success': False, 'detail': 'Вы уже отправили запрос по этой заявке'},
                status=status.HTTP_409_CONFLICT,
            )

        notification = Notification.objects.create(
            recipient=contact_request.receiver,
            type=Notification.TYPE_CONTACT_REQUEST_CREATED,
            contact_request=contact_request,
            payload={
                'bid_title': contact_request.bid.title,
                'sender_first_name': contact_request.sender.first_name,
            },
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_user_{contact_request.receiver.id}',
            {
                'type': 'notification_created',
                'payload': {
                    'id': notification.id,
                    'type': notification.type,
                    'contact_request_id': contact_request.id,
                    'data': {
                        'bid_title': contact_request.bid.title,
                        'sender_first_name': contact_request.sender.first_name,
                    },
                    'created_at': notification.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                },
            },
        )

        return Response(
            {'success': True, 'contact_request': ContactRequestSerializer(contact_request).data},
            status=status.HTTP_201_CREATED,
        )


class ContactRequestDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            cr = ContactRequest.objects.select_related('bid', 'sender', 'receiver').get(pk=pk)
        except ContactRequest.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Объект не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user != cr.sender and request.user != cr.receiver:
            return Response(
                {'success': False, 'detail': 'Объект не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({'success': True, 'contact_request': ContactRequestSerializer(cr).data})


class ContactRequestReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            cr = ContactRequest.objects.get(pk=pk)
        except ContactRequest.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Объект не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user != cr.sender and request.user != cr.receiver:
            return Response(
                {'success': False, 'detail': 'Объект не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user == cr.sender:
            return Response(
                {'success': False, 'detail': 'Недостаточно прав'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not cr.is_read:
            cr.is_read = True
            cr.save(update_fields=['is_read', 'updated_at'])

        return Response({'success': True, 'contact_request': ContactRequestSerializer(cr).data})
