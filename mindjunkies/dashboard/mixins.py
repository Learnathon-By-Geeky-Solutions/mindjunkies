from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


from django.urls import reverse

class CustomPermissionRequiredMixin:
    permission_required = None  # Must be overridden in subclasses

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("account_login"))  # Redirect unauthenticated users to login
        if not request.user.has_perm(self.permission_required):
            return redirect(reverse("verification_wait"))  # Redirect unauthorized users
        return super().dispatch(request, *args, **kwargs)
