# from importlib.resources import path
import sys, os.path
import uuid
import threading
from concurrent.futures import Future

from celery import shared_task
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from Business.UserPackage.Member import Member
from Service.DTO.GuestDTO import GuestDTO
from Service.DTO.MemberDTO import MemberDTO
from Service.MemberService import MemberService
from Service.RoleService import RoleService
from Service.UserService import UserService


# def call_with_future(fn, future, args, kwargs):
#     try:
#         result = fn(*args, **kwargs)
#         future.set_result(result)
#     except Exception as exc:
#         future.set_exception(exc)
#
#
# def threaded(fn):
#     def wrapper(*args, **kwargs):
#         future = Future()
#         threading.Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
#         try:
#             return future.result()
#         except:
#             raise future.exception()
#
#     return wrapper

role_service = RoleService()
member_service = MemberService()
user_service = UserService()
from .forms import SignupForm, LoginForm, CreateStoreForm

user = user_service.enterSystem().getData()
stores = []


def home_page(request):
    global user
    # print(user)
    if isinstance(user, GuestDTO):
        title = "Welcome Guest!"
    else:
        title = "Welcome " + user.getMemberName() + "!"
    context = {"title": title, "user": user}
    return render(request, "home.html", context)


def signup_page(request):
    global user_service
    global member_service
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
        answer = user_service.memberSignUp(username, password, phone, account_num, branch_num, country, city, street,
                                           apartment_num, zip_code)
        if not answer.isError():
            return HttpResponseRedirect("/")
    return render(request, "form.html", context)


def login_page(request):
    global user_service
    global member_service
    global user
    form = LoginForm(request.POST or None)
    if form.is_valid():
        form = LoginForm()
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is not None and password is not None:
        answer = user_service.memberLogin(username, password)
        if not answer.isError():
            user = answer.getData()
        return HttpResponseRedirect("/")
    context = {
        "title": "Login",
        "form": form
    }
    return render(request, "form.html", context)


def my_stores_page(request):
    if isinstance(user, GuestDTO):
        usertype = True
        title = "Please login to see your stores page"
    else:
        usertype = False
        title = "My Stores"
    context = {"title": title, "usertype": usertype, "user": user, "stores": stores}
    return render(request, "my_stores.html", context)


def create_store_page(request):
    global user_service
    global member_service
    global user
    global stores
    form = CreateStoreForm(request.POST or None)
    if form.is_valid():
        form = CreateStoreForm()
    storeName = request.POST.get("storeName")
    account_num = request.POST.get("account_num")
    branch_num = request.POST.get("branch_num")
    country = request.POST.get("country")
    city = request.POST.get("city")
    street = request.POST.get("street")
    apartment_num = request.POST.get("apartment_num")
    zip_code = request.POST.get("zip_code")
    if storeName is not None:
        answer = member_service.createStore(storeName, user.getMemberId(), account_num, branch_num, country, city,
                                            street,
                                            apartment_num, zip_code)
        if not answer.isError():
            stores.append(answer.getData())
        return HttpResponseRedirect("/my_stores")
    context = {
        "title": "Create New Store",
        "form": form
    }
    return render(request, "form.html", context)


def store_page(request, slug):
    answer = role_service.getRolesInformation(int(slug), user.getMemberId())
    if not answer.isError():
        permissions = answer.getData()
        return render(request, "store.html", {"permissions": permissions[0]})
