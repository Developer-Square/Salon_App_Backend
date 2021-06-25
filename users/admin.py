from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from.models import NewUser, Stylist, NewUserProfile, PhoneOTP

class UserAdminConfig(UserAdmin):
    model = NewUser
    ordering = ('-start_date',)
    search_fields = ('email', 'user_name', 'first_name',)
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')

    #fields to be listed in django admin
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'phone_number','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),

    )
    # The add_fieldsets class variable is used to define the fields that will be displayed on the create user page.
    #The classes key sets any custom CSS classes we want to apply to the form section.
    # The fields key sets the fields you wish to display in your form.
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig,)

class StylistAdminConfig(UserAdmin):
    model = NewUser
    ordering = ('-start_date',)
    search_fields = ('email', 'username', 'first_name','location',)
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff', 'location',)

    #fields to be listed in django admin
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'phone_number', 'location',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),

    )
    # The add_fieldsets class variable is used to define the fields that will be displayed on the create user page.
    #The classes key sets any custom CSS classes we want to apply to the form section.
    # The fields key sets the fields you wish to display in your form.
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name','location', 'password1', 'password2')}
         ),
    )


admin.site.register(Stylist, StylistAdminConfig)


admin.site.register(NewUserProfile)

admin.site.register(PhoneOTP)