from django.urls import path
from account import views


urlpatterns = [
   path('verify/otp/reset-password/', views.VerifyResetPasswordOTPView.as_view(), name = 'verify-otp-for-password-reset'),
   path('reset-password/', views.ResetPasswordView.as_view(), name = 'password-reset')
]