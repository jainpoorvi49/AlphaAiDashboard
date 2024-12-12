# user/serializers.py
from rest_framework import serializers
from .models import NewUser

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['user_id', 'password', 'mobile_number', 'broker_name']    
