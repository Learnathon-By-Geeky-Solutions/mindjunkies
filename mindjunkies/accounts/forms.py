from django import forms
from cloudinary.forms import CloudinaryFileField
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .models import User



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
