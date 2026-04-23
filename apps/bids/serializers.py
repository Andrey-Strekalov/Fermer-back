from django.utils import timezone
from rest_framework import serializers

from apps.users.serializers import CurrentUserSerializer
from .models import Bid


class BidCreateSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError('Title is required')
        return value

    def validate_quality(self, value: str) -> str:
        return value.strip()

    def validate_region(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Region is required')
        return value

    def validate_comment(self, value: str) -> str:
        return value.strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_volume(self, value):
        if value <= 0:
            raise serializers.ValidationError('Volume must be greater than 0')
        return value

    def create(self, validated_data):
        author = self.context['author']
        return Bid.objects.create(
            author=author,
            published_at=timezone.now(),
            **validated_data,
        )


class BidAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='first_name', read_only=True)


class BidListItemSerializer(serializers.ModelSerializer):
    author = BidAuthorSerializer(read_only=True)

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
            'published_at',
            'author',
        )

