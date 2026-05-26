from django.utils import timezone
from rest_framework import serializers

from apps.users.serializers import CurrentUserSerializer
from .models import Bid


class _BidWritableFieldsSerializer(serializers.ModelSerializer):
    """Общие поля и валидация для создания и частичного обновления заявки."""

    class Meta:
        model = Bid
        fields = (
            'type',
            'title',
            'quality',
            'price',
            'volume',
            'region',
            'comment',
        )

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Название обязательно')
        return value

    def validate_quality(self, value: str) -> str:
        return value.strip()

    def validate_region(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Регион обязателен')
        return value

    def validate_comment(self, value: str) -> str:
        return value.strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Цена должна быть больше 0')
        return value

    def validate_volume(self, value):
        if value <= 0:
            raise serializers.ValidationError('Объем должен быть больше 0')
        return value


class BidCreateSerializer(_BidWritableFieldsSerializer):
    def create(self, validated_data):
        author = self.context['author']
        return Bid.objects.create(
            author=author,
            published_at=timezone.now(),
            **validated_data,
        )


class BidUpdateSerializer(_BidWritableFieldsSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if validated_data:
            instance.save(update_fields=list(validated_data.keys()))
        return instance


class BidListItemSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = (
            'id',
            'type',
            'title',
            'quality',
            'price',
            'volume',
            'region',
            'comment',
            'is_archived',
            'published_at',
            'author',
        )


class BidSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = (
            'id',
            'type',
            'title',
            'quality',
            'price',
            'volume',
            'region',
            'comment',
            'is_archived',
            'published_at',
            'author',
        )
