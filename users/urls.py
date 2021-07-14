from django.urls import path, include
from .views import ( LoginUser, RegisterUser, StylistCreateView, DeleteUserProfile, DeleteStylistProfile, GetAnyUserProfile,
                    GetUsers, UpdateUserProfile, GetStylistProfile, GetAllStylists, UpdateStylistProfile, 
                    VerifyPhone_OTP, ResetPassword, VerifyEmailAfterSignUp )
from rest_framework_simplejwt.views import ( TokenRefreshView )

app_name = 'users'

urlpatterns = [
    # token authentication
    path('login/', LoginUser.as_view(), name ='login' ), #log in phone
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh token
    
    # veryfy phone number
    path('verify_phone_number/', VerifyPhone_OTP.as_view(), name ='verify' ), #Verify phone
    path('verify_email/', VerifyEmailAfterSignUp.as_view(), name ='verify' ), #send phone number for reseting

  
    # reset password
    path('reset_password/', ResetPassword.as_view(), name ='verify' ), #send phone number for reseting

    #users end points
    path('register/', RegisterUser.as_view(), name ="register"), #Creates a new user  
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
