from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import User, Requisites

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


class RequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisites
        fields = (
            'company_name', 'legal_address', 'inn', 'ogrn',
            'bik', 'bank_name', 'checking_account', 'correspondent_account',
            'phone', 'fax', 'email',
        )

    def validate_inn(self, value: str) -> str:
        if not value:
            return value
        if not value.isdigit():
            raise serializers.ValidationError('ИНН должен содержать только цифры.')
        if len(value) not in (10, 12):
            raise serializers.ValidationError('ИНН должен содержать 10 цифр (юрлицо) или 12 цифр (ИП).')
        return value

    def validate_ogrn(self, value: str) -> str:
        if not value:
            return value
        if not value.isdigit():
            raise serializers.ValidationError('ОГРН должен содержать только цифры.')
        if len(value) not in (13, 15):
            raise serializers.ValidationError('ОГРН должен содержать 13 цифр (юрлицо) или 15 цифр (ИП).')
        return value

    def validate_bik(self, value: str) -> str:
        if not value:
            return value
        if not value.isdigit():
            raise serializers.ValidationError('БИК должен содержать только цифры.')
        if len(value) != 9:
            raise serializers.ValidationError('БИК должен содержать ровно 9 цифр.')
        return value

    def validate_checking_account(self, value: str) -> str:
        if not value:
            return value
        if not value.isdigit():
            raise serializers.ValidationError('Расчётный счёт должен содержать только цифры.')
        if len(value) != 20:
            raise serializers.ValidationError('Расчётный счёт должен содержать ровно 20 цифр.')
        return value

    def validate_correspondent_account(self, value: str) -> str:
        if not value:
            return value
        if not value.isdigit():
            raise serializers.ValidationError('Корреспондентский счёт должен содержать только цифры.')
        if len(value) != 20:
            raise serializers.ValidationError('Корреспондентский счёт должен содержать ровно 20 цифр.')
        return value

    def validate_email(self, value: str) -> str:
        if not value:
            return value
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('Введите корректный email адрес.')
        return value