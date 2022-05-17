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
    assignee_name = forms.CharField()


class RemoveForm(forms.Form):
    owner_name = forms.CharField()


class UpdateProductForm(forms.Form):
    name = forms.CharField()
    category = forms.CharField()
    price = forms.IntegerField()


class AddProductForm(forms.Form):
    name = forms.CharField()
    category = forms.CharField()
    price = forms.IntegerField()
    keywords = forms.CharField()


class AddProductToCartForm(forms.Form):
    quantity = forms.IntegerField()


class PurchaseProductForm(forms.Form):
    accountNumber = forms.IntegerField()
    branch = forms.IntegerField()


class AddProductQuantity(forms.Form):
    quantity = forms.IntegerField()


rules = (("store", "Store"), ("category", "Category"), ("product", "Product"))
types = (("simple", "Simple"), ("quantity", "Quantity"), ("price", "Price"), ("weight", "Weight"))
decide = ((0, "First"), (1, "Second"))


# class AddDiscountForm(forms.Form):
#     rule_context = forms.ChoiceField(choices=rules, widget=forms.Select(attrs={'style': 'width:190px'}))
#     rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
#     percent = forms.IntegerField()
#     category = forms.CharField()
#     product_ID = forms.IntegerField(required=False, label="Product ID")
#     min_value = forms.IntegerField()
#     max_value = forms.IntegerField()


class AddCondition(forms.Form):
    ID_1 = forms.IntegerField()
    ID_2 = forms.IntegerField()


class AddRule(forms.Form):
    rule_context = forms.ChoiceField(choices=rules, widget=forms.Select(attrs={'style': 'width:190px'}))
    rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
    category = forms.CharField(required=False, label="Category")
    product_ID = forms.IntegerField(required=False, label="Product ID")
    min_value = forms.IntegerField()
    max_value = forms.IntegerField()


class AddSimpleDiscount_Store(forms.Form):  # done
    # rule_context = forms.ChoiceField(choices=rules, widget=forms.Select(attrs={'style': 'width:190px'}))
    # rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
    percent = forms.FloatField()


class AddSimpleConditionDiscount_Store(forms.Form):  # done
    # rule_context = forms.ChoiceField(choices=rules, widget=forms.Select(attrs={'style': 'width:190px'}))
    rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
    percent = forms.FloatField()
    min_value = forms.IntegerField()
    max_value = forms.IntegerField()


class AddSimpleDiscount_Category(forms.Form):  # done
    percent = forms.FloatField()
    category = forms.CharField()


class AddSimpleConditionDiscount_Category(forms.Form):  # done
    rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
    percent = forms.FloatField()
    category = forms.CharField()
    min_value = forms.IntegerField()
    max_value = forms.IntegerField()


class AddSimpleDiscount_Product(forms.Form):  # done
    percent = forms.FloatField()
    product_ID = forms.IntegerField(required=False, label="Product ID")


class AddSimpleConditionDiscount_Product(forms.Form):  # done
    rule_type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={'style': 'width:190px'}))
    percent = forms.FloatField()
    product_ID = forms.IntegerField(required=False, label="Product ID")
    min_value = forms.IntegerField()
    max_value = forms.IntegerField()


class AddConditionDiscountXor(forms.Form):
    discount_ID = forms.IntegerField()
    rule_ID1 = forms.IntegerField()
    rule_ID2 = forms.IntegerField()
    decide = forms.ChoiceField(choices=decide, widget=forms.Select(attrs={'style': 'width:190px'}))


class AddConditionDiscountAndOr(forms.Form):
    discount_ID = forms.IntegerField()
    rule_ID1 = forms.IntegerField()
    rule_ID2 = forms.IntegerField()


class RemoveDiscount(forms.Form):
    discount_ID = forms.IntegerField()
