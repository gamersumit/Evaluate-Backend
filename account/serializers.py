from rest_framework import serializers
from .models import User
from utils.utils import AccountUtils


class StudentUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length = 8, write_only = True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'avatar',
            'password',
        ]

    def validate_password(self, value):
       return AccountUtils.validate_password(value)



class TeacherUserDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'is_teacher',
        ]

    def validate_password(self, value):
       return AccountUtils.validate_password(value)

    def validate_is_teacher(self, value):
        return True