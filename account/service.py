from os import stat
from .models import ForgotPasswordOTP, User, MailVerificationOTP
from .serializers import ForgotPasswordOTPSerializer, MailVerificationOTPSerializer
from utils.utils import AccountUtils, CommonUtils
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class AccountService :
  
  @staticmethod
  def IsEmailExist(email):
        return User.objects.filter(email = email).exists()
  
  @staticmethod
  def get_otp_for_mail_verification(user):
    try : 
      otp = AccountUtils.otp_generator()
      data = {'otp' : otp, 'user' : user.id}
      
      if MailVerificationOTP.objects.filter(user = user.id).exists():
         otp = MailVerificationOTP.objects.get(user = user.id)
         CommonUtils.SerializerUpdate(obj = otp, data=data, serializer_class=MailVerificationOTPSerializer).save()
      
      else :  
        CommonUtils.SerializerCreate(data=data, serializer_class = MailVerificationOTPSerializer).save()
      
      return otp
    
    except Exception as e:
      raise Exception('Unexpected error occured while generating otp')
    
  
  @staticmethod
  def verify_mail(otp, email):
      if not AccountService.IsEmailExist(email):
        raise Exception('mail not found')
      
      user = User.objects.get(email = email)
      
      if not MailVerificationOTP.objects.filter(user = user.id).exists():
          raise Exception('try resending otp')
      
      obj = MailVerificationOTP.objects.get(user = user.id)
      
      five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
          
      if obj.updated_at < five_minutes_ago:
          raise Exception('otp expired')
      
      if obj.otp != int(otp):
          raise Exception('incorrect otp')  
        
      user.is_verified = True
      user.save()
      
  @staticmethod
  def verify_reset_password_otp(otp, email):
      if not AccountService.IsEmailExist(email):
        raise Exception('mail not found')
      
      user = User.objects.get(email = email)
      
      if not ForgotPasswordOTP.objects.filter(user = user.id).exists():
          raise Exception('try resending otp')
      
      obj = ForgotPasswordOTP.objects.get(user = user.id)
      
      five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
          
      if obj.updated_at < five_minutes_ago:
          raise Exception('otp expired')
      
      if obj.otp != int(otp):
          raise Exception('incorrect otp')  
      
      return user  
     
          
  @staticmethod
  def login_user(password, email):
    if not User.objects.filter(email = email).exists() :
      raise Exception('Invalid Email')
    
    user = authenticate(password = password, username = email)
    
    if not user:
      raise Exception('Incorrect Password')
    
    if not user.is_verified :
      raise Exception('Non verified User')
    
    token, created = Token.objects.get_or_create(user=user)
    return user, token
  
  @staticmethod
  def create_forgot_password_otp(email):
  
    user = User.objects.get(email = email)
    otp = AccountUtils.otp_generator()
    data = {'otp' : otp, 'user' : user.id}
    
    if ForgotPasswordOTP.objects.filter(user = user.id).exists():
        otp = ForgotPasswordOTP.objects.get(user = user.id)
        CommonUtils.SerializerUpdate(obj = otp, data=data, serializer_class=ForgotPasswordOTPSerializer).save()

    else :  
      CommonUtils.SerializerCreate(data=data, serializer_class =ForgotPasswordOTPSerializer).save()
    
    return otp
  
      
    
    
    