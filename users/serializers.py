from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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
        
        

class RegisterUserSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    username =  serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    

    class Meta:
        model= NewUser
        fields = ('email','username', 'first_name', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    
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
    
    
    