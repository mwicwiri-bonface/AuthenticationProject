# user/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, Profile


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
