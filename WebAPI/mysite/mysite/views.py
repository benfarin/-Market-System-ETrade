# from importlib.resources import path
import sys, os
from django.http import HttpResponse
from django.shortcuts import render

# p = os.path.abspath('.')
# sys.path.insert(1, p)
# # sys.path.append(os.path.abspath(os.path.join('..../Service')))
# print(sys.path)
from Service.UserService import *
from .forms import SignupForm, LoginForm
class View:
    def __init__(self):
        self.__user_service = UserService()

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


    def login_page(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            print(form.changed_data)
            form = LoginForm()
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        self.__user_service.memberLogin(username, password)
        context = {
            "title": "Login",
            "form": form
        }
        return render(request, "form.html", context)
