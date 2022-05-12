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
from django.contrib import messages

from Business.UserPackage.Member import Member
from Service.DTO.GuestDTO import GuestDTO
from Service.DTO.MemberDTO import MemberDTO
from Service.MemberService import MemberService
from Service.RoleService import RoleService
from Service.UserService import UserService

role_service = RoleService()
member_service = MemberService()
user_service = UserService()
from .forms import SignupForm, LoginForm, CreateStoreForm, AppointForm, UpdateProductForm, AddProductForm, \
    AddProductToCartForm, PurchaseProductForm, AddProductQuantity

user = user_service.enterSystem().getData()
stores = []


def home_page(request):
    global user
    # print(user)
    if isinstance(user, GuestDTO):
        title = "Welcome Guest!"
    else:
        title = "Welcome " + user.getMemberName() + "!"
    all_stores = user_service.getAllStores().getData()
    context = {"title": title, "user": user, "stores": all_stores}
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
        messages.warning(request, answer.getError())
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
            print(user.getUserID())
            return HttpResponseRedirect("/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Login",
        "form": form
    }
    return render(request, "form.html", context)


def logout(request):
    global user
    if isinstance(user, MemberDTO):
        member_service.logoutMember(user.getMemberName())
        user = user_service.enterSystem().getData()
    return HttpResponseRedirect("/")


def my_stores_page(request):
    if isinstance(user, GuestDTO):
        usertype = True
        title = "Please login to see your stores page"
    else:
        usertype = False
        title = "My Stores"
    stores = user_service.getAllStoresOfUser(user.getUserID()).getData()
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
    store_name = request.POST.get("storeName")
    account_num = request.POST.get("account_num")
    branch_num = request.POST.get("branch_num")
    country = request.POST.get("country")
    city = request.POST.get("city")
    street = request.POST.get("street")
    apartment_num = request.POST.get("apartment_num")
    zip_code = request.POST.get("zip_code")
    if store_name is not None:
        answer = member_service.createStore(store_name, user.getUserID(), account_num, branch_num, country, city,
                                            street,
                                            apartment_num, zip_code)
        if not answer.isError():
            # stores.append(answer.getData())
            return HttpResponseRedirect("/my_stores")
        messages.warning(request, answer.getError())
    context = {
        "title": "Create New Store",
        "form": form
    }
    return render(request, "form.html", context)


def store_page(request, slug):
    store = user_service.getStore(int(slug)).getData()
    answer = role_service.getRolesInformation(int(slug), user.getUserID())
    if not answer.isError():
        permissions = answer.getData()
        for permission in permissions:
            if permission.getUserId() == user.getUserID():
                context = {"permissions": permission, "items": store.getProductsAsList()}
                return render(request, "store.html", context)
    context = {"permissions": [], "items": store.getProductsAsList()}
    return render(request, "store.html", context)


def store_products_management(request, slug, slug2):
    return render(request, "products_manage.html", {})


def appoint_manager(request, slug):
    global user
    form = AppointForm(request.POST or None)
    if form.is_valid():
        form = AppointForm()
    assignee_id = request.POST.get("assignee_name")
    if assignee_id is not None:
        answer = role_service.appointManagerToStore(int(slug), user.getUserID(), assignee_id)
        if not answer.isError():
            role_service.setRolesInformationPermission(int(slug), user.getUserID(), assignee_id)
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Appoint Store Manager",
        "form": form
    }
    return render(request, "form.html", context)


def appoint_Owner(request, slug):
    global user
    form = AppointForm(request.POST or None)
    if form.is_valid():
        form = AppointForm()
    assingeeID = request.POST.get("assingeeID")
    if assingeeID is not None:
        answer = role_service.appointOwnerToStore(int(slug), user.getUserID(), assingeeID)
        if not answer.isError():
            role_service.setRolesInformationPermission(int(slug), user.getUserID(), assingeeID)
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Appoint Store Owner",
        "form": form
    }
    return render(request, "form.html", context)


# def update_product(request, slug):
#     form = UpdateProductForm(request.POST or None)
#     if form.is_valid():
#         form = UpdateProductForm()
#     name = request.POST.get("name")
#     category = request.POST.get("category")
#     price = request.POST.get("price")
#     if name is not None:
#         answer = role_service.updateProductName(user.getMemberId, int(slug), )

def add_product(request, slug):
    form = AddProductForm(request.POST or None)
    if form.is_valid():
        form = AddProductForm()
    name = request.POST.get("name")
    category = request.POST.get("category")
    price = request.POST.get("price")
    keywords = request.POST.get("keywords")
    if name is not None:
        answer = role_service.addProductToStore(int(slug), user.getUserID(), name, int(price), category, keywords)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Product",
        "form": form
    }
    return render(request, "form.html", context)


def get_cart(request):
    answer = user_service.getCart(user.getUserID())
    bags = []
    cart = []
    if not answer.isError():
        cart = answer.getData()
        for bag in cart.getAllBags().values():
            bags.append(bag)
    context = {"title": "Cart", "bags": bags, "cart": cart}
    return render(request, "cart.html", context)


def add_to_cart_page(request, slug, slug2):
    form = AddProductToCartForm(request.POST or None)
    if form.is_valid():
        form = AddProductToCartForm()
    quantity = request.POST.get("quantity")
    if quantity is not None:
        answer = user_service.addProductToCart(user.getUserID(), int(slug), int(slug2), int(quantity))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Product",
        "form": form
    }
    return render(request, "form.html", context)


def purchase_cart(request):
    form = PurchaseProductForm(request.POST or None)
    if form.is_valid():
        form = PurchaseProductForm()
    accountNumber = request.POST.get("accountNumber")
    branch = request.POST.get("branch")
    if accountNumber is not None:
        answer = user_service.purchaseCart(user.getUserID(), int(accountNumber), int(branch))
        if not answer.isError():
            return HttpResponseRedirect("/cart/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Purchase Cart",
        "form": form
    }
    return render(request, "form.html", context)


def search_view(request):
    q = request.GET.get('q', None)
    context = {"query": q}
    searches = []
    if q is not None:
        if len(q.split("-")) == 2:
            search = user_service.getProductPriceRange(int(q.split("-")[0]), int(q.split("-")[1]))
            if not search.isError():
                searches += (search.getData())
        search = user_service.getProductByName(q)
        if not search.isError():
            searches += (search.getData())
        search = user_service.getProductByCategory(q)
        if not search.isError():
            searches += (search.getData())
        search = user_service.getProductByKeyword(q)
        if not search.isError():
            searches += (search.getData())
        context['findings'] = searches
    return render(request, 'searches.html', context)


def show_history(request, slug):
    answer = role_service.getPurchaseHistoryInformation(int(slug), user.getUserID())
    transactions = []
    if not answer.isError():
        purchases = answer.getData()
        for purchase in purchases:
            transactions.append(purchase)
    context = {"title": "Purchases History", "transactions": transactions}
    return render(request, "history.html", context)


def product_update(request, slug, slug2):
    form = UpdateProductForm(request.POST or None)
    if form.is_valid():
        form = UpdateProductForm()
    name = request.POST.get("name")
    category = request.POST.get("category")
    price = request.POST.get("price")
    if name is not None and category is not None and price is not None:
        answer1 = role_service.updateProductName(user.getUserID(), int(slug), int(slug2), name)
        answer2 = role_service.updateProductCategory(user.getUserID(), int(slug), int(slug2), category)
        answer3 = role_service.updateProductPrice(user.getUserID(), int(slug), int(slug2), int(price))
        if not answer1.isError() and not answer2.isError() and not answer3.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        if answer1.isError():
            messages.warning(request, answer1.getError())
        if answer1.isError():
            messages.warning(request, answer2.getError())
        if answer1.isError():
            messages.warning(request, answer3.getError())
    context = {
        "title": "Purchase Cart",
        "form": form
    }
    return render(request, "form.html", context)


def remove_product(request, slug, slug2):
    answer = role_service.removeProductFromStore(int(slug), user.getUserID(), int(slug2))
    store = user_service.getStore(int(slug)).getData()
    if not answer.isError():
        return HttpResponseRedirect("/store/" + slug + "/")
    messages.warning(request, answer.getError())


def add_quantity(request, slug, slug2):
    form = AddProductQuantity(request.POST or None)
    if form.is_valid():
        form = AddProductQuantity()
    quantity = request.POST.get("quantity")
    if quantity is not None:
        answer = role_service.addProductQuantityToStore(int(slug), user.getUserID(), int(slug2), int(quantity))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Product Quantity",
        "form": form
    }
    return render(request, "form.html", context)
