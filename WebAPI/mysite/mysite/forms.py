from random import choice, choices
from django import forms
# from django_countries.fields import CountryField

countries = (
        ('israel', 'Israel'),
        ('united states', 'United States'),
        ('united kingdom', 'United Kingdom'),
        ('canada', 'Canada'),
        ('france', 'France'),
        ('germany', 'Germany'),
        ('spain', 'Spain'),
        ('japan', 'Japan'),
        ('china', 'China'),
        )

class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    phone = forms.CharField()
    account_num = forms.IntegerField()
    branch_num = forms.IntegerField()
    country = forms.ChoiceField(choices= countries)
    city = forms.CharField()
    street = forms.CharField()
    apartment_num = forms.IntegerField()
    zip_code = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
