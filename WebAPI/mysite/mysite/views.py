# from importlib.resources import path
import sys, os.path
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from Service.UserService import UserService

user_service = UserService()

from .forms import SignupForm, LoginForm


def home_page(request):
    context = {"title": "Welcome to my website"}
    return render(request, "home.html", context)


def signup_page(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        print(form.changed_data)
        form = SignupForm()
    context = {
        "title": "Sign Up",
        "form": form
    }
    return render(request, "form.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        print(form.changed_data)
        form = LoginForm()
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
    if username is not None and password is not None:
        user_service.memberLogin(username, password)
    context = {
        "title": "Login",
        "form": form
    }
    return render(request, "form.html", context)
