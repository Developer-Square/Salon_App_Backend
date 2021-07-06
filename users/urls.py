from django.urls import path, include
from .views import ( CustomUserCreate,StylistCreateView, DeleteUserProfile, DeleteStylistProfile, CustomTokenView, GetAnyUserProfile,
                    GetLoggedInUserProfile, GetUsers, UpdateUserProfile, GetStylistProfile, GetAllStylists, UpdateStylistProfile, 
                    VerifyPhone_OTP, VerifyOTPCode,  SendPhoneToGetOTPCode )


app_name = 'users'

urlpatterns = [
    # token authentication
    path('login/', CustomTokenView.as_view(), name ='login' ), #login 
  
    # veryfy phone number
    path('verify_phone_number/', VerifyPhone_OTP.as_view(), name ='verify' ), #Verify phone
  
    # reset password
    path('reset/send_phone/', SendPhoneToGetOTPCode.as_view(), name ='verify' ), #send phone number for reseting
    path('reset/send_otp_and_password/', VerifyOTPCode.as_view(), name ='verify' ), #login code + new password

 
    #users end points
    path('register/', CustomUserCreate.as_view(), name ="register"), #Creates a new user  
    path('profile/', GetLoggedInUserProfile.as_view(), name="user_profile"), # Get details of currently logged in user.
    path('profile/update/', UpdateUserProfile.as_view(), name="update_profile"), #update details of currently logged in user
    path('profile/delete/', DeleteUserProfile.as_view(), name="delete_profile"), #delete user
    path('<int:id>/', GetAnyUserProfile.as_view(), name="stylist_profile"), # view profile of any user
    
    #stylist endpoint 

    path('stylist/register/', StylistCreateView.as_view(), name="stylist_register"), # salonist register endpoint
    path('stylist/profile/<int:stylist_id>/', GetStylistProfile.as_view(), name="stylist_profile"), # salonist profile endpoint
    path('stylist/profile/update/', UpdateStylistProfile.as_view(), name="stylist_profile_update"), # salonist profile update endpoint
    path('stylist/profile/delete/', DeleteStylistProfile.as_view(), name="stylist_delete_profile"), # salonist delete account endpoint
    
    
    #admin endpoint
    
    path('all_users/', GetUsers.as_view(), name="all_users"), # get all users
    path('all_stylists/', GetAllStylists.as_view(), name="all_stylists"), # get all stylists
     
    
]
