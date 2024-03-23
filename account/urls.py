from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    # path('logout/', views.user_logout_view, name = 'logout'),
    # path('send_verification_email/', views.send_verification_email_view, name = 'send_verification_email'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('token/verify/', views.VerifyTokenView.as_view(), name = 'token-verify'),
    # path('otp/', views.)
]