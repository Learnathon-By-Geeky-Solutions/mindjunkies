from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PaymentGateway, Transaction


class TransactionAdmin(ModelAdmin):
    list_display = ("name", "card_no", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("currency", "status")


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PaymentGateway)
