from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("account_login")
        return redirect("verification_wait")
