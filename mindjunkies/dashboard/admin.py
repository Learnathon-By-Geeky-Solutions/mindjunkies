# Register your models here.
from django.contrib import admin
from .models import TeacherVerification

@admin.register(TeacherVerification)
class TeacherVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "email", "phone", "address", "verified")
    actions = ["approve_teacher", "disapprove_teacher"]

    def approve_teacher(self, request, queryset):
        for obj in queryset:
            obj.is_verified = True
            obj.save()
            obj.user.is_teacher = True  # Grant teacher permission
            obj.user.save()
        self.message_user(request, "Selected users have been approved as teachers.")
    approve_teacher.short_description = "Approve selected teachers"

    def disapprove_teacher(self, request, queryset):
        for obj in queryset:
            obj.is_verified = False
            obj.save()
            obj.user.is_teacher = False  # Revoke teacher permission
            obj.user.save()
        self.message_user(request, "Selected users have been disapproved as teachers.")
    disapprove_teacher.short_description = "Disapprove selected teachers"