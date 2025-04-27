from cloudinary.forms import CloudinaryFileField
from django import forms
from django.forms import ModelForm

from .models import Profile, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ProfileUpdateForm(ModelForm):
    avatar = CloudinaryFileField(required=False)

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "birthday", "phone_number", "address"]
