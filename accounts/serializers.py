from rest_framework import serializers, validators
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Account:
        return Account.objects.create_user(**validated_data)
    
    class Meta:
        model = Account
        fields = ["id", "username", "password", "email", "is_superuser"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [validators.UniqueValidator(queryset=Account.objects.all(), message="A user with that username already exists.")]
            },
            }