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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'role', 'company_logo', 'date_joined')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'company_logo')

    def validate_first_name(self, value: str) -> str:
        return value.strip()

    def validate_last_name(self, value: str) -> str:
        return value.strip()

    def validate_role(self, value: str) -> str:
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f'Некорректная роль. Допустимые значения: {", ".join(valid_roles)}'
            )
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if validated_data:
            instance.save(update_fields=list(validated_data.keys()))
        return instance