from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _

import uuid
import random


class CustomAccountManager(BaseUserManager):
    #This is custom model manager is for creating users and superusers.
    
    def create_superuser(self, email,  username, first_name, password, **other_fields):
        # creating a superuser
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
            
        return self.create_user(email, username, first_name,  password, **other_fields)
    
    
    def create_user(self,email, username, first_name,  password, **other_fields):
        #creating a user
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        if not username:
            raise ValueError(_('You must provide a Username address'))
        
        
        
        email = self.normalize_email(email) # @gmail === @GMAIL
        user =  self.model(email=email, username=username, 
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
class AbstractUser(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True )
    first_name = models.CharField(max_length=100, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False) # people who can access admin
    is_active = models.BooleanField(default=True )
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    id = models.AutoField(primary_key=True)
    newuser_uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)

    def __str__(self):
        return f"{self.first_name}"
    
    class Meta:
        ordering = ["-created_at"]
        
    class Meta:
        abstract = True
        


class NewUser( AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True )
    first_name = models.CharField(max_length=100, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False) # people who can access admin
    is_active = models.BooleanField(default=True )
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    id = models.AutoField(primary_key=True)
    newuser_uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)
    
    
    #custom model manager
    objects = CustomAccountManager()
    
    # replacing username with email  to login
    USERNAME_FIELD = 'email'
    
    # failure to innput below fields will result to an error
    REQUIRED_FIELDS = ['username', 'first_name', ]
    
    def __str__(self):
        return f"{self.first_name}"
    
    class Meta:
        ordering = ["-created_at"]


class NewUserProfile(models.Model):
    user = models.OneToOneField(NewUser, related_name="profile_picture", on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="images/profile_pics", blank=True, null=True)
    
    
    

class Stylist(NewUser):
    
    is_stylist = models.BooleanField(default=True)
    location = models.CharField(max_length=10, default="Nairobi")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null = True )
    stylist_id = models.IntegerField(auto_created=True, unique=True, default=1)
    
    def save(self, *args, **kwargs):
        self.stylist_id += self.stylist_id
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        ordering = ["-created_at",]


class PhoneOTP(models.Model):
    pass
    number = models.CharField(max_length=5, blank=True, null=True, unique=True)
    user = models.OneToOneField(NewUser,related_name="code", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        user = self.user
        if user:
            PhoneOTP.objects.filter(user=user).delete()
        numberList =  [x for x in range(10)]
        code = []
        for i in range(5):
            num =  random.choice(numberList)
            code.append(num)
        code_string = "".join(str(item) for item in code)
        self.number = code_string
        
        super().save(*args, **kwargs)



class StylistReview(models.Model):
    # related name is like a pseudo column
    stylistreview_id = models.AutoField(primary_key=True)
    stylist = models.ForeignKey(Stylist, on_delete=models.SET_NULL, null=True, related_name="stylist_review")
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, related_name="review")
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)



    

