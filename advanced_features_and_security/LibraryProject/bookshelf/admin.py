from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser  # Specify the custom user model
    list_display = ("email", "date_of_birth", "is_staff", "is_superuser")  # Fields visible in the list view
    fieldsets = (
        (None, {"fields": ("email", "password")}),  # Basic user details
        ("Personal Info", {"fields": ("date_of_birth", "profile_photo")}),  # Custom fields
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "date_of_birth", "profile_photo", "password1", "password2"),
        }),
    )
    ordering = ("email",)  # Order users by email
    search_fields = ("email",)  # Enable search by email

admin.site.register(CustomUser, CustomUserAdmin)  # Register the custom user model



