from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import ProfileUpdateForm
from .models import Profile


@method_decorator(require_GET, name='dispatch')
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form: ProfileUpdateForm) -> HttpResponse:
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
