from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    # path('logout/', views.user_logout_view, name = 'logout'),
    path('mail/verify/', views.VerifyMailView.as_view(), name = 'verify_email'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('token/verify/', views.VerifyTokenView.as_view(), name = 'token-verify'),
    path('send/otp/reset-password/', views.SendPasswordResetOTPView.as_view(), name = 'send-otp-for-password-reset'),
    path('verify/otp/reset-password/', views.VerifyResetPasswordOTPView.as_view(), name = 'verify-otp-for-password-reset')
]