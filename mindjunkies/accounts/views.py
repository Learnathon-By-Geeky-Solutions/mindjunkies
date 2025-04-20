from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from .forms import ProfileUpdateForm, UserForm
from .models import Profile


@method_decorator(require_GET, name="dispatch")
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        user_form = UserForm(instance=request.user)
        return render(
            request,
            self.template_name,
            {"profile_form": profile_form, "user_form": user_form},
        )

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"profile_form": profile_form, "user_form": user_form},
        )
