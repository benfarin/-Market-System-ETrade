from django import forms


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    phone = forms.CharField()
    account_num = forms.IntegerField()
    branch_num = forms.IntegerField()
    country = forms.CharField()
    city = forms.CharField()
    street = forms.CharField()
    apartment_num = forms.IntegerField()
    zip_code = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
