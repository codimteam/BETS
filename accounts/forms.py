from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from mainApp.models import *
from django.db import models



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model= User
        fields = {
            'first_name',
            'last_name',
            'username',
            'email',
        }


class EditProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields = {
            'first_name',
            'last_name',
            'email'
        }


class ProfileForm(forms.ModelForm):
    YEARS = [x for x in range(1940,2020)]
    phone_regex = RegexValidator(regex='\+?1?\d{11,15}', message="Format-'+877777777' 15 digits allowed")
    phone_number = forms.CharField(validators=[phone_regex], max_length=15)
    birth_date=forms.DateField(label="Enter your birth date:", initial='1995-09-09', widget=forms.SelectDateWidget(years=YEARS))
    city = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'city',
            'birth_date'
        ]