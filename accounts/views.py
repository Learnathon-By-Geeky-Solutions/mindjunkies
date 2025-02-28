from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProfileUpdateForm
from .models import Profile


def profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'profile.html')


def edit_profile(request: HttpRequest) -> HttpResponse:
    user_profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user_profile)

    context = {
        "form": form
    }
    return render(request, 'edit_profile.html', context)
