from django.db import models

class Transaction(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    account_id = models.CharField(max_length=128, db_index=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")

    raw_payload = models.JSONField()

    risk_score = models.FloatField()
    risk_level = models.CharField(max_length=8, choices=RiskLevel.choices)
    reasons = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["risk_level", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.account_id} - {self.amount} {self.currency} ({self.risk_level})"
