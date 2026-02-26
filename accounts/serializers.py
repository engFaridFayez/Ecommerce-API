from rest_framework import serializers
from axes.handlers.proxy import AxesProxyHandler

from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    is_blocked = serializers.SerializerMethodField()

    def get_is_blocked(self,obj):
        request = self.context['request']
        return AxesProxyHandler.is_locked(request,{'username':obj.username})

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'last_login',
            'is_staff',
            'is_active',
            'is_blocked',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "confirm_password"
        ]
        extra_kwargs= {'password':{'write_only':True}}

    def validate(self,attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        return attrs
    
    def create(self,validate_data):
        password = validate_data.pop('password')
        validate_data.pop('confirm_password')
        user = CustomUser(**validate_data)
        user.set_password(password)
        user.save()
        return user