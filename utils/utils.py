import random
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re
from rest_framework.authtoken.models import Token


class AccountUtils :

    @staticmethod
    def validate_password(value):
    # valid password : >= 8 char, must contains lower at least 1 char of each 
    # lower(alpha), upper(alpha), (number), (symbols)
    
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if  not re.search("\d", value) :
            raise serializers.ValidationError("Password must contains a number 0 to 9")
        
        if not re.search("[a-z]", value) :
            raise serializers.ValidationError("Password must contain a lowercase letter ")
        
        if not re.search("[A-Z]", value) :
            raise serializers.ValidationError("Password must contain a uppercase letter")
        
        if not re.search(r"[@#$%^&*()\-_+=.]", value):
            raise serializers.ValidationError("Password must contain a special character(@,#,$,%,^,&,*,(,),-,_,+,=,.)")

        return make_password(value)    # return hashed password
    
    @staticmethod
    def getUserFromToken(token):
        try :
            token = Token.objects.get(key = token)
            user = token.user
            return user
        
        except Exception as e :
            raise Exception(str(e))
    
    @staticmethod
    def otp_generator():
        otp = random.randint(100001, 999999)
        return otp
    

class MailUtils:
    
    def __init__(self, subject, body, emails):
        self.subject = subject
        self.body = body
        self.emails = emails # list
        
    @staticmethod
    def SendVerificationMail(otp, user):
        MailUtils(subject = 'Evaluate Email Verification', body = f'Hii  {user.username},\n\n\n\nYour OTP:   {otp}\n\nOTP will expire after 5minutes.\n\nThankyou', emails=[user.email]).send()
    
    def SendForgotPasswordOTPMail(otp, user):
        MailUtils(subject = 'Password Reset Mail', body = f'Hii  {user.username},\n\n\n\nYour OTP:   {otp}\n\nOTP will expire after 5minutes.\n\nThankyou', emails=[user.email]).send()
    
    
    def send(self):
        print('sending mail')
        print('to: ', self.emails)
        print('from: ', settings.EMAIL_HOST_USER)
        send_mail(
            self.subject, 
            self.body,
            settings.EMAIL_HOST_USER,
            self.emails,
            fail_silently=False)
    


class CommonUtils :
    @staticmethod  
    def SerializerCreate(data, serializer_class):
        serializer = serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        return serializer
    
    def SerializerUpdate(obj, data, serializer_class):
        serializer = serializer_class(obj, data = data, partial = True)
        serializer.is_valid(raise_exception = True)
        return serializer
          
    

        