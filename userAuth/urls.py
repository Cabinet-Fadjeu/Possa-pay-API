from django.urls import path,include

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView
# )

from . import views
# from .views import ChangePasswordView

app_name = "userAuth"

urlpatterns = [
    # Update user profile image
    # path('user-images-profile/<uuid:user_id>/', views.userProfileImageUpdate, name='user-image-profile'),

    # Checking user Secret code
    # path('check-secret/', views.check_secret_code),
    path('set-secret/', views.set_secret_code, name='set-secret'),
    # path('set-secret/<str:request_type>/<uuid:user_id>/', views.set_user_secret, name='set_user_secret'),
    # #sevices demande
    # path('service/demande/<uuid:user_id>/', views.service_demand, name='service_demand'), 
    # #creat service
    # path('service/create/<uuid:user_id>/', views.create_service, name='create_service'),
    #reception des fond
    # path('service/receive/', views.reception, name='reception'),
    # User registration Routes
    path('register/', views.register_view, name='register'),
    # User login Routes
    path('login/', views.login_view,name='login'),
    # User token refresh Routes
    # path('token/refresh-token/', TokenRefreshView.as_view(),name='refresh_token'),
    # User logout Routes
    path('logout/', views.logout_view,name='logout'),
    # path('login/', views.login),
    # User view details
    # path('user-detail/<uuid:id>/', views.userDetail),

    # AUTH for password
    # Changing password
    # path('change-password/<uuid:id>/', ChangePasswordView.as_view(),name='change_password'),
    # Password reset
    # path('password-reset/', include('django_rest_passwordreset.urls'), name='password_reset'),

    # AUTH for Phone Number
    # Setting phone number
    # path('phone-number/<uuid:id>/', views.setPhoneNumber,name='set_phone_number'),
    # # Confirming phone number
    # path('phone-number-confirmation/<uuid:id>/', views.confirmPhoneNumber,name='confirm_phone_number'),

    # AUTH for Email
    # Changing email
    # path('email-change/<uuid:id>/', views.changeEmail, name='changing_email'),
    # # Validating email
    # path('email-verification/<uuid:id>/', views.verifyEmail, name='verify_email'),

    # WALLET
    # Get user Wallet
    # path('user-wallets/<uuid:user_id>/', views.get_wallet, name='user_wallet')
   

]