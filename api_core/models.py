from django.db import models
import uuid
from django.utils.translation import gettext as _
from userAuth.models import CustomUser, Service, Compte


# Create your models here.
class apiCoreTransactions(models.Model):
    id  = models.UUIDField(_('id'), default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL ,null=True, blank=True)
    service = models.ForeignKey(Service,on_delete=models.SET_NULL ,null=True, blank=True)
    
    amount = models.DecimalField(_('Paid amount'), max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(_('Currency'),max_length=10, null=True, blank=True)
    payment_type = models.CharField(_('Payment type'),max_length=50, null=True, blank=True)
    
    productId = models.CharField(_('Product unique identifier'),max_length=250, null=True, blank=True)
    productName = models.CharField(_('Product Name'),max_length=200, null=True, blank=True)

    transaction_status = models.CharField(_('Transaction status'),max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Transaction date',blank=True, null=True)


    class Meta :
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.transaction_status