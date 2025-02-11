# from django.contrib import admin
# from userAuth.models import CustomUser, Wallet

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email',)

# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('id','user_id', 'amount' )

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Wallet,WalletAdmin)

# # Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Wallet,Service, Compte

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id','username', 'email', 'is_active','country')
    list_filter = ('is_active',)
    readonly_fields = ('email',)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id','user_id', 'amount', )
    readonly_fields = ('id',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'name', 'compte', 'allowed_hosts')

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount',)