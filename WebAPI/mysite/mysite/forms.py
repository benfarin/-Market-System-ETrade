from random import choice, choices
from django import forms
# from django_countries.fields import CountryField
from django_countries.data import COUNTRIES


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    phone = forms.CharField()
    account_num = forms.IntegerField()
    branch_num = forms.IntegerField()
    country = forms.ChoiceField(choices=COUNTRIES.items(), widget=forms.Select(attrs={'style': 'width:190px'}))
    city = forms.CharField()
    street = forms.CharField()
    apartment_num = forms.IntegerField()
    zip_code = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreateStoreForm(forms.Form):
    storeName = forms.CharField()
    accountNumber = forms.IntegerField()
    brunch = forms.IntegerField()
    country = forms.ChoiceField(choices=COUNTRIES.items(), widget=forms.Select(attrs={'style': 'width:190px'}))
    city = forms.CharField()
    street = forms.CharField()
    apartment_num = forms.IntegerField()
    zip_code = forms.IntegerField()


class AppointForm(forms.Form):
    assingeeID = forms.CharField()


class UpdateProductForm(forms.Form):
    name = forms.CharField()
    category = forms.CharField()
    price = forms.IntegerField()


class AddProductForm(forms.Form):
    name = forms.CharField()
    category = forms.CharField()
    price = forms.IntegerField()
    keywords = forms.CharField()