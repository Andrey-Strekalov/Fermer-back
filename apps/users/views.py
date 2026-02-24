from django.shortcuts import render

import random


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PhoneOTP
from .models import User
from .serializers import ConfirmCodeSerializer
from .serializers import RequestCodeSerializer
from .constants import OTP_CODE_LENGTH, OTP_TTL_SECONDS

from datetime import timedelta
from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken




class RequestCodeView(APIView):
    def post(self, request):

        serializer = RequestCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        code = ''.join(
            str(random.randint(0, 9))
            for _ in range(OTP_CODE_LENGTH)
        )

        PhoneOTP.objects.create(
            phone_number=phone,
            code=code
        )

        return Response(
            {
                "success": True,
                "code": code,
                "expires_in": OTP_TTL_SECONDS
            },
            status=status.HTTP_200_OK
        )




class ConfirmCodeView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp = PhoneOTP.objects.filter(
            phone_number=phone,
            code=code,
            is_used=False
        ).order_by('-created_at').first()

        if not otp:
            return Response(
                {"success": False, "detail": "Invalid code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        expires_in = otp.created_at + timedelta(seconds=OTP_TTL_SECONDS)

        if timezone.now() > expires_in:
            return Response(
                {"success": False, "detail": "Code expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        otp.is_used = True
        otp.save(update_fields=['is_used'])

        user, _ = User.objects.get_or_create(
            phone_number=phone,
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
            status=status.HTTP_200_OK
        )