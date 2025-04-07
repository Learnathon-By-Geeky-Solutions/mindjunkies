from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "is_staff", "is_teacher")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Details",
            {
                "fields": ["uuid", "is_teacher"],
            },
        ),
    )
    readonly_fields = ("uuid",)


@admin.register(Profile)
class CustomProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user", "birthday", "phone_number")
    search_fields = ("user__username", "user__email")
    list_filter = ("birthday", "phone_number")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "birthday",
                    "bio",
                    "avatar",
                    "phone_number",
                    "address",
                )
            },
        ),
    )
