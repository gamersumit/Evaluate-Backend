
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re
import base64
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings

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
    def sendLink(user, subject, message): 
        try :     
            send_mail(
                subject, 
                message,
                settings.EMAIL_HOST_USER,
                user.email,
                fail_silently=False 
                )
            
            return True
    
        except Exception as e :
            raise Exception(str(e))

class CommonUtils :
    @staticmethod
    def base64_to_image(base64_image, image_name):
        try :
            format, imgstr = base64_image.split(';base64,') 
            ext = format.split('/')[-1] 
            image = ContentFile(base64.b64decode(imgstr), name=image_name+'.' + ext)
            return image
       
        except :
            return None 
        