from django.urls import path
from .views import GoogleSocialAuthView

app_name='social_auth'

urlpatterns = [
    # token authentication
    path('google/', GoogleSocialAuthView.as_view(), name ='google_login' ), #log in using google
]