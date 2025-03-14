from cloudinary.forms import CloudinaryFileField
from django.forms import ModelForm

from .models import Profile


class ProfileUpdateForm(ModelForm):
    avatar = CloudinaryFileField()

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "birthday", "phone_number", "address"]
