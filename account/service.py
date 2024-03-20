from os import stat
from .models import User, MailVerificationOTP
from .serializers import MailVerificationOTPSerializer
from utils.utils import AccountUtils
from django.utils import timezone

class AccountService :
  
  @staticmethod
  def IsEmailExist(email):
        return User.objects.filter(email = email).exists()
  
  @staticmethod
  def get_otp_for_mail_verification(user):
    try : 
      otp = AccountUtils.otp_generator()
      data = {'otp' : otp, 'user' : user.id}
      serializer = MailVerificationOTPSerializer(data = data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return otp
    
    except Exception as e:
      print(str(e))
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
          
       