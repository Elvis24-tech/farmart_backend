# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# This allows you to see and edit the Profile directly on the User change page
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    # These fields will be displayed in the list view of users
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    
    # This adds 'user_type' and 'phone_number' to the filter sidebar
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    
    # This adds custom fields to the edit/creation forms in the admin
    # It extends the default UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom User Info', {'fields': ('user_type', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom User Info', {'fields': ('user_type', 'phone_number', 'email')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Unregister the default User model if it was somehow registered, then register our custom one
# admin.site.unregister(User) # This is usually not needed but safe to have
admin.site.register(User, CustomUserAdmin)