from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser): 
    # receiver will be called before deletion of object
    username = models.CharField(max_length = 50)
    avatar = models.URLField(null = True, blank = True)
    email = models.EmailField(unique=True, null = False, blank = False)
    is_teacher = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)

    # password in serializer
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username