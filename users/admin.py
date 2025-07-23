# users/admin.py
from django.contrib import admin
from .models import User, Profile

# It's also good practice to use the UserAdmin for more features
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    # Add or customize fields shown in the admin list/edit pages
    list_display = ['email', 'username', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'phone_number', 'email')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
