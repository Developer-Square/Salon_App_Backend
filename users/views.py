import json
import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,  IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth.hashers import make_password   

from drf_social_oauth2.views import TokenView
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.signals import app_authorized


from .models import NewUser, Stylist, PhoneOTP
from .serializers import (RegisterUserSerializer, RegisterStylistSerializer, UserSerializer, StylistSerializer,
                UserProfileSerializer, )
from .utils import Util, get_random_code

'''
Authentication
'''


class CustomTokenView(TokenView,):
    '''
    Log in a user, returns token and user details, like id, phone_number, email
    '''

    def post(self, request, *args, **kwargs):

        mutable_data = request.data.copy()
        request._request.POST = request._request.POST.copy()
        for key, value in mutable_data.items():
            request._request.POST[key] = value
            url, headers, body, status = self.create_token_response(
                request._request)
            if status == 200:
                body = json.loads(body)
                access_token = body.get("access_token")
                if access_token is not None:
                    token = get_access_token_model().objects.get(
                        token=access_token)
                    app_authorized.send(
                        sender=self, request=request,
                        token=token)
                    body['user'] = {
                        'id': token.user.id,
                        'username': token.user.username,
                        'email': token.user.email,
                        'first_name': token.user.first_name,
                    
                    }
                    body = json.dumps(body)
            response = Response(data=json.loads(body), status=status)
            for k, v in headers.items():
                response[k] = v
            return response

   
class CustomUserCreate(APIView):
    '''  
    registering a new user
    
    '''
    permission_classes = [AllowAny,]
    def post(self, request, format='json'):
        serializer = RegisterUserSerializer(data=request.data)
        
        
        if serializer.is_valid(raise_exception=True):
            
            user = serializer.save()
            if user:
                
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        
class VerifyPhone_OTP(APIView):
    '''  
    class will verify the phone number given by the use using OTP.
    It has to take place after access token is issued. eg after account creation or after creation and login
    data = phonenumber
    
    '''
    permission_classes = [AllowAny,]
    
    
    def get(self, request, *args, **kwargs):
        
        '''
         user has to be logged in after creating account
         a phone otp table is created with user and code
         after get request a user is sent a sms code
        
        '''
     
        if request.user.is_anonymous == True:
            return Response("get access token")
        else:
            user = self.request.user
            if user:
                phone = user.phone_number
                num = get_random_code()
                PhoneOTP.objects.create(user=user, number=num)
                number = user.code.number 
                # send sms to user containing number recepient is phone
                sms = f"{user.username} - {number}"
                return Response(sms)
            else:
                return Response("First log in")

    def post(self, request, *args, **kwargs):
        '''
        posting the code sent to our phone. 
        confirms with the one created in the db during get request
        '''
        user = self.request.user
        if user:
            code = user.code.number 
            number = request.data["number"]
            if str(code) == number:
                
                message = {'detail': 'verified'}
                return Response(message, status=status.HTTP_201_CREATED, )   
            else :
                message = {'detail': 'verification_failed'}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            
        else:
            return Response("First log in")

class SendPhoneToGetOTPCode(APIView):
    '''
    user is supposed to fill the phone number and post request 
    random number is then generated and used to create a phoneOTP object
    A message is then sent to the username containing the otp code
    
    '''
    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data['phone_number']
        try:
            user = NewUser.objects.get(phone_number = phone_number)
        except:
            return Response("usser does not exist")
        if user:
           
            print(user)
            num = get_random_code()
            
            PhoneOTP.objects.create(user=user, number=num)
            number = user.code.number 
            sms = f"{user} - {number}"
            
            print (user.username, "sent a message", number)
            # send message
            return Response(sms)


class VerifyOTPCode(APIView):
    permission_classes = [AllowAny,]
    
    def put(self, request, *args, **kwargs):
        data = request.data
        number = data['number']
        password = data['password']
        number = str(number)
        try:       
            otp = PhoneOTP.objects.get(number = number)
        except:
            return Response("otp does not exist")
        print("otp", otp)
        user = otp.user
        print("name -", user.username)
        if user:
           
            user.password = make_password(data["password"])
            user.save()
     
        print("new_password set", user.password)
        
        return Response("new_password set")
        
    
 
class GetLoggedInUserProfile(APIView):
    '''  
    This class GET the  details of the currently logged in user.    
    '''
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get(self, request): 
        try:
            current_user = self.request.user
            serializer = UserProfileSerializer(current_user, many=False)
            return Response(serializer.data)
        except :
            return Response("you are not logged in")
        
        
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
    
        
            
        
        
        
        
    
        
            