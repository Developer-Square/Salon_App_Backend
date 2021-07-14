# 555068933656-haou46l4vec87gf7akedbudgm653c1a6.apps.googleusercontent.com

import json
import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,  IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


from .models import NewUser, Stylist, PhoneOTP
from .serializers import (LoginSerializer, RegisterUserSerializer, RegisterStylistSerializer, UserSerializer, StylistSerializer,
                UserProfileSerializer, )
from .utils import Util, get_random_code

class LoginUser(APIView):
    '''
    Authentication
    '''
    schema = AutoSchema(manual_fields=[
    coreapi.Field(
        "data",
        required=True,
        location="body",
        description='{"email":str, "password":str}',
        schema=coreschema.Object()
        ),
        ])
   
    permission_classes = [AllowAny, ]
    serializer_class = [LoginSerializer, ]
    
    def post(self, request):
      
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
            

class RegisterUser(APIView):
    '''  
    registering a new user
    
    '''
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "data",
            required=True,
            location="body",
            description='{"email":str, "úsername":str, "password":str,  "password":str}',
            schema=coreschema.Object()
        ),
    ])
    permission_classes = [AllowAny,]
    def post(self, request, format='json'):
        
        data = request.data
        
        entered_username =  NewUser.objects.filter(username = data['username'])
                         
        entered_email = NewUser.objects.filter(email=data['email'] )
        try: 
            entered_phone_number = NewUser.objects.filter(phone_number = data['phone_number'] )    
        except:
            pass
        
        if entered_username:
            return Response("This username already exist")
        if entered_email:
            return Response("This email already exist")
        try: 
            if entered_phone_number:
                return Response("This Phone number already exist")
        except:
            pass
 

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
               
                user_data = serializer.data
                try:
                    user = NewUser.objects.get(email=user_data['email'] )
                except:
                    return Response(user_data['email'], 'email does not esist')
                    
                num = get_random_code()
            
                PhoneOTP.objects.create(user=user, number=num)
                otp_code = user.code.number 
                email_message = "Hello "+ user.username + " use this code - " + otp_code  + " to verify your email"
                print(user.email)
                data = {'email_subject': 'Verify email', 'email_body': email_message, 'to_email': user.email, }
                Util.send_email(data)
                
                sms_data = "Hello "+  user.username +  " use this code " + otp_code +  " to verigy your phone number"
                
                Util.send_sms(sms_data)
                
                print ('Hi', user.username, "we have sent you a code on submitted email to verify this email", otp_code)
                
                token = RefreshToken.for_user(user).access_token
        
                return Response(user_data, status=status.HTTP_201_CREATED)
           
            
            
            
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailAfterSignUp(APIView):
    '''  
    class will verify the email given by the use using OTP.
    It has to take place after access token is issued. eg after account creation or after creation and login
    data = phonenumber
    
    '''
    permission_classes = [AllowAny,]
    

    def post(self, request, *args, **kwargs):
        '''
        send code to backend
        '''
        user = self.request.user
        if user:    
            code_in_db = user.code.number # existing on db, created on signup  
            try:
                otp_code = request.data["number"]  # submitted by client
            except: 
                return Response("enter code")
            if otp_code:
                if str(code_in_db) == str(otp_code):
                    return Response('Email is verified', status=status.HTTP_201_CREATED, )  
                    if not user.email_is_verified:
                        user.email_is_verified = True
                        user.save()    
                        return Response('Email verification successful', status=status.HTTP_200_OK)
                else :
                  
                    return Response('Email verification_failed', status=status.HTTP_403_FORBIDDEN)
            else:
                return Response('enter the code', status=status.HTTP_403_FORBIDDEN)      
        else:
            return Response("First log in")

        
        
class VerifyPhone_OTP(APIView):
    '''  
    class will verify the phone number given by the use using OTP.
    It has to take place after access token is issued. eg after account creation or after creation and login
    data = phonenumber
    
    '''
    permission_classes = [AllowAny,]
    
    def post(self, request, *args, **kwargs):
        '''
        posting the code sent to THE phone. 
        confirms with the one created in the db during get request
        '''
        user = self.request.user
        if user:
            code = user.code.number 
            try:      
                otp_code = request.data["number"]
            except:
                return Response('enter the code', status=status.HTTP_403_FORBIDDEN)
        
            if str(code) == str(otp_code):
                return Response('Phone number is now veriified', status=status.HTTP_201_CREATED, )   
                if not user.phone_is_verified:
                    user.phone_is_verified = True
                    user.save()
            else :
                return Response('verification_failed', status=status.HTTP_403_FORBIDDEN)              
        else:
                return Response("First log in")


class ResetPassword(APIView): # FORGET PASSWORD 1
    '''
    user is supposed to fill the phone number and post request 
    random number is then generated and used to create a phoneOTP object
    A message is then sent to the username containing the otp code
    
    '''
    def post(self, request, *args, **kwargs):
        print(request.data)
     
        try:
            phone_number = request.data['phone_number']
        except: 
            return Response(' Enter phone number' )
        try:
            user = NewUser.objects.get(phone_number = phone_number)
        except:
            return Response("user does not exist")
        if user:

            num = get_random_code()
            
            PhoneOTP.objects.create(user=user, number=num)
            otp_code = user.code.number 
            sms_data = "Hello"+  user.username+  "use this code - " + otp_code +  "to change your password"
            
            Util.send_sms(sms_data)
            
            print (user.username, "sent a message", otp_code)
            # send message
            
            return Response('We have sent you a message containing the verification number', status=status.HTTP_200_OK)
        else: 
            return Response("This phone number does not belong to ant registered user")
        
    def put(self, request, *args, **kwargs):
        try:
            number = request.data['number']
        except: 
            return Response(' Enter otp code' )
        if number:
            pass
        else:
            return Response(' Enter 111 the code' )
        try:
            password = request.data['password']
        except: 
            return Response(' Enter password' )    
        if password:
            pass
        else:
            return Response(' Enter the new password' )
        
       
        password = request.data['password']
        number = str(number)
        try:       
            otp = PhoneOTP.objects.get(number = number)
        except:
            return Response("otp does not exist")
        print("otp", otp)
        user = otp.user
        print("name -", user.username)
        if user:
        
            user.password = make_password(password)
            user.save()
    
        print("new_password set", user.password)
        
        return Response("new password set",  status=status.HTTP_200_OK)
    
            


class GetAnyUserProfile(APIView):
    '''  
    This class GET the  details of any user  
    '''
    
    permission_classes = [AllowAny,]
    
    def get_object(self, id):
        try:
            return NewUser.objects.get(id=id)
        except NewUser.DoesNotExist:
            return status.HTTP_400_BAD_REQUEST

    def get(self, request, id):
        
        user = self.get_object(id)
        print("user", user)
        serializer = UserSerializer(user)
        print("serializer", serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
     

class UpdateUserProfile(APIView):
    '''
     class for updating the currently logged in user
     all fields have to be sent from the backend.
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def put(self, request): 
        user = self.request.user
        serializer = UserSerializer(user, many=False)
   
            
        data = self.request.data
       
        user.username = data['username']
        user.first_name = data['first_name']
        user.email = data["email"]
        user.phone_number = data["phone_number"]
        
        if data["password"] !=  '':
            user.password = make_password(data["password"])
        
      
        user.save()
        return Response(serializer.data)
    
    
class DeleteUserProfile(APIView):
    '''
         User actount is deactivated once they opt to delete their account
    '''
    

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
 
    def delete(self, request ):
        user = self.request.user
        
        if user:
            try:
                user = NewUser.objects.get(id = user.id)
                user.is_active = False
                user.save()
                return Response("User deleted")
               
            except :
                return Response("User does not exist")
        else:
            return Response('Log in')
        

'''
Admin
'''           

class GetUsers(APIView):
    #This class is for the admin to view all users
    permission_classes = [IsAdminUser] 
    serializer_class = UserSerializer
    
    def get(self, request):
        users = NewUser.objects.all().filter()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class GetAllStylists(APIView):
    permission_classes = [AllowAny]
    serializer_class = StylistSerializer
    
    def get(self, request):
        stylists = Stylist.objects.all()
        serializer = StylistSerializer(stylists, many=True)
        return Response(serializer.data)
 
'''
Stylist
'''       
   
class StylistCreateView(APIView):
    '''
      registering a new stylist
    '''
   
    permission_classes = [AllowAny,]

    def post(self, request, format='json'):
        serializer = RegisterStylistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class GetStylistProfile(APIView):
    '''
     users can view any stlist profile, when stylist-id is passed as keyword argument
    '''
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = StylistSerializer
    
    def get_object(self, stylist_id):
        try:
            return Stylist.objects.get(stylist_id=stylist_id)
        except Stylist.DoesNotExist:
            return status.HTTP_400_BAD_REQUEST

    def get(self, request, stylist_id):
        
        stylist = self.get_object(stylist_id)
        print("stylist", stylist)
        serializer = StylistSerializer(stylist)
        print("serializer", serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateStylistProfile(APIView):
    '''
     class will update the currently logged in stylist
    '''
    
    permission_classes = [IsAuthenticated]
 
    def put(self, request, ):
        user = self.request.user
        if user:
            try:
                stylist = Stylist.objects.get(user.id)
                data = self.request.data
                serializer = StylistSerializer(stylist, data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response("You are not a registered stylist")
                
            
        else:
            return Response("You are not logged in")


class DeleteStylistProfile(APIView):
    '''
     User actount is deactivated once they opt to delete their account
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
 
    def delete(self, request ):
        user = self.request.user
        
        if user:
            try:
                user = Stylist.objects.get(id = user.id)
                user.is_active = False
                user.save()
                return Response("Account deleted")
               
            except :
                return Response("User does not exist")
            
        else:
            return Response('User is not logged ')
    
        
            
        
        
        
        
    
        
            