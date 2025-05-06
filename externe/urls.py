from django.urls import path,include

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView
# )

from .views import GeneratePaymentUrl, PaymentLogin


app_name = "externe"

urlpatterns = [
    #generer un lien de paiement
    path('api/payment-url/', GeneratePaymentUrl, name='payment-url'),
    #lien de paiement
    
    path('api/payment/<public_key>-<amount>-<devise>', PaymentLogin, name='payment'),
]