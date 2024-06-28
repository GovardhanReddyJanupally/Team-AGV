from .models import Employee,Deployed,Pricipal_consultant,OnbordsTable,Company_propertise
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email')  # Add any other required fields

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
            # Add other fields here as needed
        )
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Include additional fields as needed

class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs


class emp_serilizer(serializers.ModelSerializer):
    class Meta :
        model = Employee
        fields ='__all__'
        # exclude = ['']
class deply_serilizer(serializers.ModelSerializer):
    class Meta :
        model = Deployed
        fields ='__all__'
class princple_serializer(serializers.ModelSerializer):
    class Meta :
        model = Pricipal_consultant
        fields ='__all__'
class OnbordsTable_serializer(serializers.ModelSerializer):
    class Meta :
        model = OnbordsTable
        fields ='__all__'
class Company_propertise_serializer(serializers.ModelSerializer):
    class Meta:
        model =Company_propertise
        fields ="__all__"
