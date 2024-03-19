
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import User
from rest_framework.authtoken.models import Token
from utils.utils import CommonUtils, AccountUtils
import random
# Create your views here.

class RegisterView(generics.CreateAPIView) :
    queryset = User.objects.all()
    serializer_class = StudentUserSerializer








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
        
