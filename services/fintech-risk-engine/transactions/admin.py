from django.contrib import admin

from .models import Transaction
 
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account_id", "amount", "currency", "risk_level", "risk_score", "created_at")
    list_filter = ("risk_level", "currency", "created_at")
    search_fields = ("account_id",)
    readonly_fields = ("raw_payload", "risk_score", "risk_level", "reasons", "created_at")
    ordering = ("-created_at",)
