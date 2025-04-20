from django.db import models

from config.models import BaseModel
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course


class Transaction(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="transactions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.DO_NOTHING, related_name="transactions"
    )
    enrollment = models.OneToOneField(
        "courses.Enrollment",
        on_delete=models.DO_NOTHING,
        related_name="transaction",
    )

    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_id = models.CharField(max_length=15, unique=True)
    val_id = models.CharField(max_length=75)
    card_type = models.CharField(max_length=150)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_no = models.CharField(max_length=55, blank=True)
    bank_tran_id = models.CharField(max_length=155, blank=True)
    status = models.CharField(max_length=55)
    tran_date = models.DateTimeField()
    currency = models.CharField(max_length=10)
    card_issuer = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=15)
    card_issuer_country = models.CharField(max_length=55)
    card_issuer_country_code = models.CharField(max_length=55)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    verify_sign = models.CharField(max_length=155)
    verify_sign_sha2 = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=15)
    risk_title = models.CharField(max_length=25)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return self.user.username + " - " + self.course.title
    



class Balance(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="balance"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}"


class BalanceHistory(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="balance_history"
    )
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="balance_entries",
        null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.created_at}"


class PaymentGateway(models.Model):
    store_id = models.CharField(max_length=500, blank=True)
    store_pass = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Payment Gateway"
        verbose_name_plural = "Payment Gateway"

    def __str__(self):
        return self.store_id
