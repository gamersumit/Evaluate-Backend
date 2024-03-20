from os import stat
from .models import User, MailVerificationOTP
from .serializers import MailVerificationOTPSerializer
from utils.utils import AccountUtils

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