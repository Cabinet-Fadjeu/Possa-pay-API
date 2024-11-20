from django.urls import path, include

from . import views


urlpatterns = [
    # Retreat
    # path('request-retreat/', views.requestRetreat, name='request_retreat'),

    # Transfer
    path('transfer/', views.makeTransfer, name='make_transfer'),
    # path('transfer-detail/', views.getTransfersDetail, name='transfer-detail'),

    # # RECHARGE
    # path('recharge/', views.makeRecharge, name='make_transfer'),

    # # HISTORY
    # path('recharge-history/<uuid:id>/', views.getRechargeHistory, name='recharge-history'),    
    # path('transfers-history/<uuid:id>/', views.getTransfersHistory, name='transfers-history'),

]