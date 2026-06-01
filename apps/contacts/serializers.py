from rest_framework import serializers

from .models import ContactRequest


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = (
            'id', 'bid_id', 'sender_id', 'receiver_id', 'comment',
            'sender_phone_snapshot', 'sender_organization_snapshot',
            'is_read', 'created_at',
        )
        read_only_fields = fields


class ContactRequestCreateSerializer(serializers.Serializer):
    bid_id = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_comment(self, value: str) -> str:
        return value.strip()
