from django.urls import path, include

from . import views

app_name = "core"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile_view, name="profile"),
    # Retreat
    # path('request-retreat/', views.requestRetreat, name='request_retreat'),

    # Transfer
    path('transfer/', views.makeTransfer, name='make_transfer'),
    path('confirm-transaction/', views.confirmTransaction, name='confirm-transaction'),
    # path('modifier_statut/', views.modifier_statut, name='modifier_statut'),
    path('modifier_statut/<str:transaction_id>/', views.modifier_statut, name='modifier_statut'),
    # path('transfer-detail/', views.getTransfersDetail, name='transfer-detail'),

    # # RECHARGE
    path('recharge/', views.recharge_wallet, name='Recharge'),

    #solde
    path('solde/', views.solde, name='solde'),

    # # HISTORY
    # path('recharge-history/<uuid:id>/', views.getRechargeHistory, name='recharge-history'),    
    # path('transfers-history/<uuid:id>/', views.getTransfersHistory, name='transfers-history'),

    #Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    #stripe webhook
    path('stripe_webhooks/', views.stripe_webhook, name='stripe_webhooks'),

    # Payment Successful
    path("payment-completed/",  views.payment_completed_view, name="payment-completed"),

    path('api/check-payment/', views.check_payment_status, name='check_payment_status'),
    
    # Payment Failed
    path("payment-failed/", views.payment_failed_view, name="payment-failed"),

    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),

    # path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('pending/', views.pending_page, name='pending_page'),
    path('api/check-payment/', views.check_payment_status, name='check_payment_status'),
]