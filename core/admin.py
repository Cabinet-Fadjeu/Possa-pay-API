# -----Cagnotte---
from django.contrib import admin

from .models import Cagnotte,ContributionCagnotte,RechargeWallet,Transfer,Donation,Retreat,Participant,PoolRetreat

# Register your models here.
@admin.register(Cagnotte)
class CagnotteAdmin(admin.ModelAdmin):
    list_display = ('id','user','name_cagnotte', 'end_date', 'price')
    list_filter = ('end_date','date_created')



@admin.register(ContributionCagnotte)
class ContributionCagnotteAdmin(admin.ModelAdmin):
    list_display = ('id','cagnotte', 'contribution', 'currency')

# -----participant---

# Register your models here.
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id','pool','email_participant', 'amount', 'currency','date_participate')
    list_filter = ('date_participate',)
    
@admin.register(PoolRetreat)
class PoolRetreatAdmin(admin.ModelAdmin):
    list_display = ('id','retreat_status','amount', 'commission','currency')
    list_filter = ('date_created',)

# -------transaction-----

# Register your models here.
@admin.register(Retreat)
class RetreatAdmin(admin.ModelAdmin):
    list_display = ('id','amount','currency','state')
    list_filter = ('request_date',)
    readonly_fields = ('id',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id','email','amount','is_Anonymous')
    list_filter = ('deposite_date',)
    readonly_fields = ('id','first_name','email','is_Anonymous','amount','deposite_type')

@admin.register(RechargeWallet)
class CustomUserRechargeAdmin(admin.ModelAdmin):
    list_display = ('account_email','amount','sender_email', 'recharge_method')
    list_filter = ('recharge_date','amount',)
    readonly_fields = ('id','amount','recharge_method','account_email','sender_email')


@admin.register(Transfer)
class CustomUserTransferAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'amount','receiver_email')
    list_filter = ('transfer_date',)
    readonly_fields = ('id','amount','user','receiver_email')