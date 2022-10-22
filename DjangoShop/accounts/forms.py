from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(forms.Form):
    otp_choices = (('e', 'email'), ('p', 'phone'))
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=11)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    otp_way = forms.ChoiceField(choices=otp_choices)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number is exist')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username is exist')
        return username


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label='Phone Number')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


