from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone_number"]}),
        ("Permissions", {"fields": ["is_active", "is_staff"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "phone_number", "password1", "password2"],
            },
        ),
    ]   
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = []

admin.site.register(User, UserAdmin)
