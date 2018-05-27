from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Business, Profile, Neighbourhood, Message

class SignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model=User
        fields=('username', 'email', 'password1', 'password2')

class Creatprofileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name', 'profile_image','neighbourhood', 'email']

class Createneighbourhood(forms.ModelForm):
    class Meta:
        model=Neighbourhood
        fields=['neighbourhood_name', 'location', 'occupation_count']

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=['business_name','business_type','neighbourhood', 'business_email','phone_number']

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['message']
