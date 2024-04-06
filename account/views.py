
from venv import create
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from .models import ForgotPasswordOTP, User
from .service import AccountService
from rest_framework.authtoken.models import Token
from utils.utils import AccountUtils, CommonUtils, MailUtils
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LogoutView as DRFLogoutView
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class RegisterView(generics.CreateAPIView) :
    queryset = User.objects.all()
    serializer_class = StudentUserSerializer

    @swagger_auto_schema(
        operation_summary = 'Register Student',
        operation_description='Register with your email and password which is securely managed',
        )
        
    def post(self, request):
        try:
            raise Exception('Testing')
            email = request.data['email']
            if AccountService.IsEmailExist(email):
                user = User.objects.get(email=email)
            
            else : 
                # register user
                user = CommonUtils.SerializerCreate(data = request.data, serializer_class=self.serializer_class).save()
            
            
            if user.is_verified:
                return Response({'message' : 'email already exists'}, status = status.HTTP_403_FORBIDDEN)

            
            CommonUtils.SerializerUpdate(user, data = request.data, serializer_class=self.serializer_class).save()
         
            # generate otp for mail verification and save it to database
            otp  = AccountService.get_otp_for_mail_verification(user)
            # send mail verification otp
            MailUtils.SendVerificationMail(otp, user)
            return Response({'message' : 'OTP SENT'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(str(e))
            return Response({'message' : 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



class VerifyMailView(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_summary = 'Verify Mail',
        )
    def post(self, request):
        try :
            otp = request.data['otp']
            email = request.data['email']
            
            try : 
                AccountService.verify_mail(otp = otp, email = email)
            
            except Exception as e :
                return Response({'message' : str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            return Response({'message' : 'Verification Succesful'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView) :
    serializer_class = StudentUserSerializer
    
    @swagger_auto_schema(
        operation_summary = 'Login User',
        )
    def post(self, request, *args, **kwargs) :
        try :
            print(request.data)
            email = request.data['email']
            password = request.data['password']       

            try :
                user, token = AccountService.login_user(email = email, password = password)
                return Response({'message' : {'token' : str(token), 'is_teacher' : user.is_teacher}}, status=status.HTTP_200_OK)
            
            except Exception as e:
                print(str(e))
                return Response({'message' : str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except :
            return Response({'message' : 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


#  logout view        
class LogoutView(generics.RetrieveAPIView) :
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key = token)
        token.delete()
        return Response({'status': True, 'message': 'User Logout Successfully'}, status = 200)
        
class SendPasswordResetOTPView(generics.CreateAPIView):
    serializer_class = ForgotPasswordOTPSerializer
    queryset = ForgotPasswordOTP.objects.all()
    
    @swagger_auto_schema(
        operation_summary = 'Send OTP for password resetting',
        )
    def post(self, request):
        try:
            email = request.data['email']
            if not AccountService.IsEmailExist(email):
                raise Exception('Invalid email')
            
            user = User.objects.get(email = email)

            if not user.is_verified :
                raise Exception('Invalid email')
            # generate otp for mail verification and save it to database
            otp  = AccountService.create_forgot_password_otp(email)
            
            # send mail verification otp
            MailUtils.SendForgotPasswordOTPMail(otp, user)
            
            return Response({'message' : 'OTP SENT'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyResetPasswordOTPView(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_summary = 'Verify OTP for password resetting',
        )
    def post(self, request):
        try :
            print(request.data)
            otp = request.data['otp']
            email = request.data['email']
            
            try : 
               print("tyring")
               user = AccountService.verify_reset_password_otp(otp = otp, email = email)
               print(user)
               token, created = Token.objects.get_or_create(user=user) 
               print(token, created)
               
            except Exception as e :
                return Response({'message' : str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            
            return Response({'message' : {'token' : str(token)}}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = 'Reset Password',
        )
    def post(self, request):
        try :
            user = AccountUtils.getUserFromToken(request.headers['Authorization'].split(" ")[1])
            data = {'password' : request.data['password']}
            CommonUtils.SerializerUpdate(user, data=data, serializer_class=StudentUserSerializer).save()
            return Response({'message' : 'password reset successfully'}, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = 'Verify Token',
        tags=['Token'],
        )
    def get(self, request):
        return Response({'message' : 'Verified User'}, status= status.HTTP_200_OK)




class PatchLogoutView(DRFLogoutView):
    """
    Djano 5 does not have GET logout route anymore, so Django Rest Framework UI can't log out.
    This is a workaround until Django Rest Framework implements POST logout.
    Details: https://github.com/encode/django-rest-framework/issues/9206
    """
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)