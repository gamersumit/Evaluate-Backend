
from venv import create
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from .models import ForgetPasswordOTP, User
from .service import AccountService
from rest_framework.authtoken.models import Token
from utils.utils import AccountUtils, CommonUtils, Mail, MailUtils
import random
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterView(generics.CreateAPIView) :
    queryset = User.objects.all()
    serializer_class = StudentUserSerializer

    def post(self, request):
        try:
            email = request.data['email']
            if AccountService.IsEmailExist(email):
                user = User.objects.get(email=email)
            
            else : 
                # register user
                user = CommonUtils.SerializerCreate(data = request.data, serializer_class=self.serializer_class).save()
            
            
            if user.is_verified:
                return Response({'message' : 'email already exists'}, status=status.HTTP_403_FORBIDDEN)

            
            CommonUtils.SerializerUpdate(user, data = request.data, serializer_class=self.serializer_class).save()
         
            # generate otp for mail verification and save it to database
            otp  = AccountService.get_otp_for_mail_verification(user)
            
            # send mail verification otp
            MailUtils.SendVerificationMail(otp, user)
            
            return Response({'message' : 'OTP SENT'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyMailView(generics.GenericAPIView):
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
    def post(self, request, *args, **kwargs) :
        try :
            email = request.data['email']
            password = request.data['password']       

            try :
                user, token = AccountService.login_user(email = email, password = password)
                Response({'message' : {'token' : token, 'is_teacher' : user.is_teacher}}, status=status.HTTP_200_OK)
            
            except Exception as e:
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
    
    def post(self, request):
        try:
            email = request.data['email']
            if not AccountService.IsEmailExist(email):
                raise Exception('Invalid email')
            
            user = User.objects.get(email = email)
            # generate otp for mail verification and save it to database
            otp  = AccountService.get_otp_for_mail_verification(user)
            
            # send mail verification otp
            MailUtils.SendVerificationMail(otp, user)
            
            return Response({'message' : 'OTP SENT'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyResetPasswordOTPView(generics.GenericAPIView):
    def post(self, request):
        try :
            otp = request.data['otp']
            email = request.data['email']
            
            try : 
               user = AccountService.verify_reset_password_otp(otp = otp, email = email)
               token, created = Token.objects.get_or_create(user=user) 
               
            except Exception as e :
                return Response({'message' : str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            return Response({'message' : {'token' : token}}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message' : 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try :
            user = AccountUtils.getUserFromToken(request.headers['Authorization'].split(" ")[1])
            data = {'password' : request.data['password']}
            CommonUtils.SerializerUpdate(user, data=data, serializer_class=StudentUserSerializer).save()
            return Response({'message' : 'password reset successfully'}, status = 200)
        
        except Exception as e:
            return Response({'message': str(e)}, status = 400)