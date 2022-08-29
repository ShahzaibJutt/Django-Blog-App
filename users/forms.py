from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['email','username','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
