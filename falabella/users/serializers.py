from rest_framework import serializers
from .models import CustomUser
from .models import Address

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone', 'documento', 'password'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'documento': {'required': True},
        }

    def create(self, validated_data):
        # Llamamos a create_user del CustomUserManager
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            documento=validated_data['documento'],
            password=validated_data['password']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)#Verifica que el email brindado existe

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)  #Codificado 
    token = serializers.CharField(required=True) #Token generado
    new_password = serializers.CharField(required=True, write_only=True) #Restablecer solo de escritura

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country', 'is_default']



