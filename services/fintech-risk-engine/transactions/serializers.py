from rest_framework import serializers

from .models import Transaction


class ScoreRequestSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=128)
    tx_amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    currency = serializers.CharField(max_length=8, required=False, default="USD")
    timestamp = serializers.DateTimeField(required=False)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id", "account_id", "amount", "currency",
            "risk_score", "risk_level", "reasons", "created_at",
        ]