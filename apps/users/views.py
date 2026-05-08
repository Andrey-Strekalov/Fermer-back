import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .models import PhoneOTP

from .serializers import ConfirmCodeSerializer
from .serializers import RequestCodeSerializer
from .serializers import CurrentUserSerializer
from .serializers import RefreshTokenRequestSerializer

from .constants import OTP_CODE_LENGTH, OTP_TTL_SECONDS

from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render
from django.shortcuts import get_object_or_404


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
                {"success": False, "detail": "Неверный код"},
                status=status.HTTP_400_BAD_REQUEST
            )

        expires_in = otp.created_at + timedelta(seconds=OTP_TTL_SECONDS)

        if timezone.now() > expires_in:
            return Response(
                {"success": False, "detail": "Срок действия кода истек"},
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


class CurrentUserView(APIView):
    authentication_classes = ()

    @staticmethod
    def unauthorized_response():
        return Response(
            {"success": False, "detail": "Не авторизован"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def get(self, request):
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)

        if header is None:
            return self.unauthorized_response()

        try:
            raw_token = jwt_auth.get_raw_token(header)
            if raw_token is None:
                return self.unauthorized_response()

            validated_token = jwt_auth.get_validated_token(raw_token)
            user = jwt_auth.get_user(validated_token)
        except Exception:
            return self.unauthorized_response()

        serializer = CurrentUserSerializer(user)
        return Response(
            {
                "success": True,
                "user": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class RefreshAccessTokenView(APIView):
    authentication_classes = ()

    @staticmethod
    def invalid_refresh_response():
        return Response(
            {"success": False, "detail": "Неверный refresh token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def post(self, request):
        serializer = RefreshTokenRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return self.invalid_refresh_response()

        refresh_token = serializer.validated_data['refresh_token']

        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh.get('user_id')
            if not user_id:
                return self.invalid_refresh_response()

            User.objects.get(pk=user_id)
            access_token = str(refresh.access_token)
        except Exception:
            return self.invalid_refresh_response()

        return Response(
            {
                "success": True,
                "access_token": access_token,
            },
            status=status.HTTP_200_OK
        )