from rest_framework import serializers

class RequestCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value: str)-> str:
        value = value.strip()

        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'")

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Invalid phone number length")

        return value

class ConfirmCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        attrs['phone']= attrs['phone'].strip()
        attrs['code'] = attrs['code'].strip()

        return attrs