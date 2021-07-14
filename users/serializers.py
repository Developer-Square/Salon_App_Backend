from django.contrib import auth

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import NewUser, Stylist, NewUserProfile, PhoneOTP



class UserSerializer(ModelSerializer):
    # used to serialize user data
    
    # .SerializerMethodField is used to return a field not in db
   
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model =NewUser
        fields = ('id','newuser_uuid', 'isAdmin', 'username', 'email', 'first_name', 'phone_number')

    
    def get_isAdmin(self, obj):
        return obj.is_staff

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
       
    class Meta:
        model = NewUserProfile
        fields = "__all__"
 
 
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=13, min_length=10, read_only=True)
    phone_number = serializers.CharField(max_length=68, min_length=6, read_only=True)
    # tokens = serializers.CharField(read_only=True)

    tokens = serializers.SerializerMethodField( read_only=True)
    # id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = NewUser
        fields = ['email', 'password', 'username', 'phone_number', 'tokens', 'id']
    
    def get_tokens(self, obj):
          
        user = NewUser.objects.get(email=obj['email'])
        
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }  
            
            
        
    def validate(self, attrs):
        email = attrs.get('email', )
        password = attrs.get('password', '')
        user = auth.authenticate(password=password, email=email)
       
        if not user:
            raise  AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise  AuthenticationFailed('Account disabled, contact admin')
        # if not user.phone_is_verified:
        #     raise  AuthenticationFailed('Phone is not verified')
        # if not user.email_is_verified:
        #     raise  AuthenticationFailed('Email is not verified')
        
        
        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'phone_number': user.phone_number,
            'tokens': user.tokens(),
            'email_is_verified': user.email_is_verified,
            'phone_is_verified': user.phone_is_verified,
        }
        
        return super().validate(attrs)
       
           
        

class RegisterUserSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    username =  serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    # phone_number = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    

    class Meta:
        model= NewUser
        fields = ('email','username', 'first_name', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}, }


    def validate(self, attrs):
        email = attrs.get('email', '')
        username  =attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return super().validate(attrs) 

    
    def create(self, validated_data):
        password = self.validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # stylist

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

        
    # stylist serializer
    
    

class RegisterStylistSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    username =  serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    

    class Meta:
        model= Stylist
        fields = ('email','username', 'first_name', 'phone_number', 'password', 'location')
        extra_kwargs = {'password': {'write_only': True}, }

    
    def create(self, validated_data):
        password = self.validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # stylist

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class StylistSerializer(ModelSerializer):
    # used to serialize user data
    
    # .SerializerMethodField is used to return a field not in db
   
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model =Stylist
        fields = ('id', 'stylist_id', 'newuser_uuid', 'isAdmin', 'username', 'email', 'first_name', "phone_number", 'location' )

    def get_isAdmin(self, obj):
        return obj.is_staff
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = UserSerializer()
    class Meta:
        model = NewUserProfile
        fields = "__all__"
    
    
    