# from importlib.resources import path
import sys, os.path
import uuid

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from Business.UserPackage.Member import Member
from Service.UserService import UserService

user_service = UserService()
from .forms import SignupForm, LoginForm

user = user_service.enterSystem()


def home_page(request):
    print(user)
    context = {"title": "Welcome to my website", "user" : user}
    return render(request, "home.html", context)


def signup_page(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form = SignupForm()
    context = {
        "title": "Sign Up",
        "form": form
    }
    username = request.POST.get("username")
    password = request.POST.get("password")
    phone = request.POST.get("phone")
    account_num = request.POST.get("account_num")
    branch_num = request.POST.get("branch_num")
    country = request.POST.get("country")
    city = request.POST.get("city")
    street = request.POST.get("street")
    apartment_num = request.POST.get("apartment_num")
    zip_code = request.POST.get("zip_code")
    if username is not None:
        user_service.memberSignUp(username, password, phone, account_num, branch_num, country, city, street,
                                  apartment_num, zip_code)
        return HttpResponseRedirect("/")
    return render(request, "form.html", context)


def login_page(request):
    global user
    form = LoginForm(request.POST or None)
    if form.is_valid():
        form = LoginForm()
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        user = user_service.memberLogin(username, password)
        return HttpResponseRedirect("/")
    context = {
        "title": "Login",
        "form": form
    }
    return render(request, "form.html", context)
