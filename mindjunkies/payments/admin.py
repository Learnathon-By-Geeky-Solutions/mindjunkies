from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PaymentGateway, Transaction


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ("name", "card_no", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("currency", "status")


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(ModelAdmin):
    list_display = ("store_id", "store_pass")
    search_fields = ("store_id",)
