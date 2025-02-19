from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Details', {
            'fields': [
                'uuid'
            ],
        }),
    )
    readonly_fields = ('uuid',)
