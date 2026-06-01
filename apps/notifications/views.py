from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = Notification.objects.filter(recipient=request.user)

        is_read_param = request.query_params.get('is_read')
        if is_read_param == 'false':
            qs = qs.filter(is_read=False)
        elif is_read_param == 'true':
            qs = qs.filter(is_read=True)

        serializer = NotificationSerializer(qs, many=True)
        data = serializer.data
        return Response({'count': len(data), 'results': data})


class NotificationReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response(
                {'success': False, 'detail': 'Объект не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user != notification.recipient:
            return Response(
                {'success': False, 'detail': 'Недостаточно прав'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=['is_read'])

        return Response({'success': True, 'notification': NotificationSerializer(notification).data})


class NotificationReadAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).update(is_read=True)

        return Response({'success': True, 'updated': updated})
