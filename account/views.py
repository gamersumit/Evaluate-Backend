
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from .models import User
from .service import AccountService
from rest_framework.authtoken.models import Token
from utils.utils import AccountUtils, CommonUtils, Mail
import random
# Create your views here.

class RegisterView(generics.CreateAPIView) :
    queryset = User.objects.all()
    serializer_class = StudentUserSerializer

    def post(self, request):
        try:
            if AccountService.IsEmailExist(request.data['email']):
                return Response({'message' : 'email already exists'}, status=status.HTTP_403_FORBIDDEN)
            
            # register user
            serializer = CommonUtils.SerializerCreate(data = request.data, serializer_class=self.serializer_class)
            user = serializer.save()    
            # generate otp for mail verification and save it to database
            otp  = AccountService.get_otp_for_mail_verification(user)
            
            # send mail verification otp
            Mail(subject = 'Email Verification Mail', body = f'OTP : {otp}', emails=[request.data['email']]).send()
            
            return Response({'message' : 'User Registered Successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(str(e))
            return Response({'message' : str(e)}, status=status.HTTP_400_BAD_REQUEST)





# class SendVerificationEmailView(generics.GenericAPIView) :
#     http_method_names = ['GET']

#     def get(self, request, *args, **kwargs):
#         otp = random.randint(100000, 999999)
#         subject = "Verification Mail from Evaluate App Team"
#         message = f"Please Don't share the OTP with anyone\n\n\n\tOTP : {otp}\n\n\nThis One Time Password is valid only for 10 minutes"

#         try : 
#             email = request.data['email']
#             user = CustomUser.objects.get(email = email)
            
#             # send mail
#             AccountUtils.sendLink(user, subject, message)

#             # yet to be implemented 
                
            
#             # # if status[0] :
#             # #     return Response({'status': True, 'data': serializer.data,'message' : 'User Registered Successfully'}, status =200)
            
#             # if status[1] == 'email not found':
#             #     return Response({'status': False, 'data': "",'message' : 'Email Not Found'}, status = 400)

#         except Exception as e:
#              return Response({'status': False, 'data': "",'message' : str(e)}, status = 400)


 # logout view // delete token       
# class LogoutView(generics.RetrieveAPIView) :
#     def get(self, request):
#         auth_header = request.headers.get('Authorization')
#         if auth_header and auth_header.startswith('Token '):
#             token = auth_header.split(' ')[1]

#             token = Token.objects.get(key = token)
#             token.delete()
#             return Response({'status': True, 'message': 'User Logout Successfully'}, status = 200)
        
#         else :
#             return Response({'status': False, 'message': 'Missing Token'}, status = 400)
        
