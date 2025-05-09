from django.contrib import admin
from .models import apiCoreTransactions
# Register your models here.

@admin.register(apiCoreTransactions)
class ApiTransAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'amount', 'currency','payment_type', 'transaction_status')
    list_filter = ('created_at',)

