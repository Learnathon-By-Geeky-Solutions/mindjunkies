# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from .models import Certificate, TeacherVerification


@admin.register(TeacherVerification)
class TeacherVerificationAdmin(ModelAdmin):
    list_display = ("user", "full_name", "email", "phone", "address", "verified")
    actions = ["approve_teacher", "disapprove_teacher"]

    def approve_teacher(self, request, queryset):
        for obj in queryset:
            obj.verified = True
            obj.save()
            print(obj.verified)
            obj.user.is_teacher = True  # Grant teacher permission
            obj.user.groups.add(
                Group.objects.get(name="Teacher")
            )  # Add to Teachers group
            obj.user.save()
        self.message_user(request, "Selected users have been approved as teachers.")

    approve_teacher.short_description = "Approve selected teachers"

    def disapprove_teacher(self, request, queryset):
        for obj in queryset:
            obj.verified = False
            obj.save()
            obj.user.is_teacher = False  # Revoke teacher permission
            obj.user.groups.remove(
                Group.objects.get(name="Teacher")
            )  # Remove from Teachers group
            obj.user.save()
        self.message_user(request, "Selected users have been disapproved as teachers.")

    disapprove_teacher.short_description = "Disapprove selected teachers"


# Register your models here.
@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ("id", "image", "description")
    search_fields = ("description",)
    list_filter = ("created_at", "updated_at")
