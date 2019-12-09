from django import forms
from .models import *
from django.contrib.auth.models import User


class PaymentForm(forms.ModelForm):
    cash = forms.DecimalField(required=True, widget=forms.TextInput)
    card_name = forms.CharField(required=True, max_length=30,  widget=forms.TextInput)
    card_number = forms.CharField(required=True, max_length=30, widget=forms.TextInput)
    exp_date = forms.CharField(required=True, max_length=15,  widget=forms.TextInput)
    cvv = forms.CharField(required=True, max_length=3,  widget=forms.TextInput)

    class Meta:
        model = Payments
        fields = [
            'cash',
            'card_name',
            'card_number',
            'exp_date',
            'cvv'
        ]




