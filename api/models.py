from django.db import models

import uuid
from django.utils.translation import gettext as _


# Create your models here.

# for definning various payment method available
class ApiPaymentGateway(models.Model):
    GATEWAY_CHOICES = [
        ("Stripe", "STRIPE"),
        ("Paypal", "PAYPAL"),
        ("Mobile Money", "MOBILE MONEY"),
        ("Possa Pay", "POSSA PAY"),
    ]

    id  = models.UUIDField(_('ID'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    payment_name = models.CharField(_("Payment Gateway"),max_length=20, choices=GATEWAY_CHOICES, unique=True)
    description = models.TextField(_("Description"),blank=True, null=True)
    is_active = models.BooleanField(_("Gateway status"),default=True)


    def __str__(self):
        return self.payment_name
    
# Api Transaction model
class ApiTransaction(models.Model):
    STATUS_CHOICES = [
        ("Pending", "PENDING"),
        ("Completed", "COMPLETED"),
        ("Failed", "FAILED"),
        ("Cancelled", "CANCELLED"),
    ]

    CURRENCY_CHOICES = [
        ("usd", "USD"),
        ("cad", "CAD"),
        ("eur", "EUR"),
        ("xaf", "XAF"),
    ]

    id  = models.UUIDField(_('ID'),default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    gateway = models.ForeignKey(ApiPaymentGateway, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency= models.CharField(max_length=5, choices=CURRENCY_CHOICES, default="usd")
    status= models.CharField(max_length=10, choices=STATUS_CHOICES, default="usd")
    transaction_id = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at")

    def __str__(self):
        return f"Transaction {self.transaction_id} ({self.status})"
