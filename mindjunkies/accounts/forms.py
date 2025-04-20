from cloudinary.forms import CloudinaryFileField
from django import forms
from django.forms import ModelForm

from .models import Profile, User


class UserForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileUpdateForm(ModelForm):
    avatar = CloudinaryFileField()

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "birthday", "phone_number", "address"]
