from rest_framework import serializers
from .models import User

class RequestCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value: str)-> str:
        value = value.strip()

        if not value.startswith('+'):
            raise serializers.ValidationError("Номер телефона должен начинаться с '+'")

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Некорректная длина номера телефона")

        return value

class ConfirmCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        attrs['phone']= attrs['phone'].strip()
        attrs['code'] = attrs['code'].strip()

        return attrs

class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(source='phone_number', read_only=True)
    name = serializers.CharField(source='first_name', read_only=True)

class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Неверный refresh token')
        return value