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
    AddProductToCartForm, PurchaseProductForm, AddProductQuantity, AddCondition, AddRule, \
    AddSimpleDiscount_Store, AddSimpleConditionDiscount_Store, AddConditionDiscountXor, AddConditionDiscountAndOr, \
    AddSimpleDiscount_Category, AddSimpleConditionDiscount_Category, AddSimpleDiscount_Product, \
    AddSimpleConditionDiscount_Product, RemoveDiscount, RemoveForm, RemoveMemberForm, StoreTransactions, \
    UserTransactions, StoreTransactionsByID

user = user_service.enterSystem().getData()
stores = []


def home_page(request):
    global user
    # print(user)
    is_admin = False
    if isinstance(user, GuestDTO):
        title = "Welcome Guest!"
    else:
        title = "Welcome " + user.getMemberName() + "!"
        is_admin = member_service.isSystemManger(user.getMemberName()).getData()
    all_stores = role_service.getAllStores().getData()
    context = {"title": title, "user": user, "stores": all_stores, "is_admin" : is_admin}
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
        answer = user_service.memberLogin(user.getUserID(), username, password)
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
    stores = role_service.getUserStores(user.getUserID()).getData()
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
    store = role_service.getStore(int(slug)).getData()
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
    assingeeID = request.POST.get("assignee_name")
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
    cart_sum = user_service.getSumAfterDiscount(user.getUserID()).getData()
    bags = []
    cart = []
    if not answer.isError():
        cart = answer.getData()
        for bag in cart.getAllBags().values():
            bags.append(bag)
    context = {"title": "Cart", "bags": bags, "cart": cart, "sum": cart_sum}
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
                if search.getData() not in searches:
                    searches += (search.getData())
        search = user_service.getProductByName(q)
        if not search.isError():
            if search.getData() not in searches:
                searches += (search.getData())
        search = user_service.getProductByCategory(q)
        if not search.isError():
            if search.getData() not in searches:
                searches += (search.getData())
        search = user_service.getProductByKeyword(q)
        if not search.isError():
            if search.getData() not in searches:
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
    store = role_service.getUserStores(int(slug)).getData()
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


def purchases_page(request):
    if isinstance(user, GuestDTO):
        usertype = True
        title = "Please login to see your purchases page"
    else:
        usertype = False
        title = "My Purchases"
    purchases = member_service.getMemberTransactions(user.getUserID()).getData()
    context = {"title": title, "usertype": usertype, "user": user, "purchases": purchases}
    return render(request, "my_purchases.html", context)


def permissions_page(request, slug):
    global user
    form = AppointForm(request.POST or None)
    if form.is_valid():
        form = AppointForm()
    assingeeID = request.POST.get("assignee_name")
    if assingeeID is not None:
        if request.method == 'POST' and 'btn1' in request.POST:
            answer = role_service.setStockManagerPermission(int(slug), user.getUserID(), assingeeID)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if request.method == 'POST' and 'btn2' in request.POST:
            answer = role_service.setAppointOwnerPermission(int(slug), user.getUserID(), assingeeID)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if request.method == 'POST' and 'btn4' in request.POST:
            answer = role_service.setChangePermission(int(slug), user.getUserID(), assingeeID)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if request.method == 'POST' and 'btn5' in request.POST:
            answer = role_service.setPurchaseHistoryInformationPermission(int(slug), user.getUserID(), assingeeID)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
    context = {
        "title": "Set Permissions",
        "form": form
    }
    return render(request, "permissions.html", context)


def remove_product_from_cart(request, slug):
    answer = user_service.removeProductFromCart(user.getUserID(), 0, int(slug))
    if not answer.isError():
        return HttpResponseRedirect("/cart/")
    messages.warning(request, answer.getError())


def close_store(request, slug):
    answer = member_service.removeStore(int(slug), user.getUserID())
    if not answer.isError():
        return HttpResponseRedirect("/my_stores/")
    messages.warning(request, answer.getError())


def discounts_page(request, slug):
    return render(request, "discounts.html")



def add_condition_add(request, slug):
    form = AddCondition(request.POST or None)
    if form.is_valid():
        form = AddCondition()
    ID_1 = request.POST.get("ID_1")
    ID_2 = request.POST.get("ID_2")
    if ID_1 is not None:
        answer = role_service.addConditionDiscountAdd(user.getUserID(), int(slug), int(ID_1), int(ID_2))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Condition ADD",
        "form": form
    }
    return render(request, "form.html", context)


def add_condition_max(request, slug):
    form = AddCondition(request.POST or None)
    if form.is_valid():
        form = AddCondition()
    ID_1 = request.POST.get("ID_1")
    ID_2 = request.POST.get("ID_2")
    if ID_1 is not None:
        answer = role_service.addConditionDiscountMax(user.getUserID(), int(slug), int(ID_1), int(ID_2))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Condition MAX",
        "form": form
    }
    return render(request, "form.html", context)


def add_rule(request, slug):
    form = AddRule(request.POST or None)
    if form.is_valid():
        form = AddRule()
    rule_context = request.POST.get("rule_context")
    rule_type = request.POST.get("rule_type")
    category = request.POST.get("category")
    product_ID = request.POST.get("product_ID")
    less_then = request.POST.get("max_value")
    bigger_then = request.POST.get("min_value")
    if rule_context == "store":
        if rule_type == "price":
            answer = role_service.createStoreTotalAmountRule(user.getUserID(), int(slug), less_then, bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if rule_type == "quantity":
            answer = role_service.createStoreQuantityRule(user.getUserID(), int(slug), less_then, bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if rule_type == "weight":
            answer = role_service.createStoreWeightRule(user.getUserID(), int(slug), less_then, bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
    if rule_context == "category":
        if rule_type == "weight":
            answer = role_service.createCategoryRule(user.getUserID(), int(slug), category, less_then, bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
    if rule_context == "product":
        if rule_type == "quantity":
            answer = role_service.createProductRule(user.getUserID(), int(slug), int(product_ID), less_then,
                                                    bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
        if rule_type == "weight":
            answer = role_service.createProductWeightRule(user.getUserID(), int(slug), int(product_ID), less_then,
                                                          bigger_then)
            if not answer.isError():
                return HttpResponseRedirect("/store/" + slug + "/")
            messages.warning(request, answer.getError())
    context = {
        "title": "Add Rule",
        "form": form
    }
    return render(request, "form.html", context)


def add_store_simple_discount(request, slug):
    form = AddSimpleDiscount_Store(request.POST or None)
    if form.is_valid():
        form = AddSimpleDiscount_Store()
    percent = request.POST.get("percent")
    if percent is not None:
        answer = role_service.addSimpleDiscount_Store(user.getUserID(), int(slug), float(percent))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Store Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_store_simple_condition_discount(request, slug):
    form = AddSimpleConditionDiscount_Store(request.POST or None)
    if form.is_valid():
        form = AddSimpleConditionDiscount_Store()
    rule_type = request.POST.get("rule_type")
    percent = request.POST.get("percent")
    less_then = request.POST.get("max_value")
    more_then = request.POST.get("min_value")
    if rule_type is not None:
        answer = role_service.addSimpleConditionDiscount_Store(user.getUserID(), int(slug), rule_type, float(percent),
                                                               less_then, more_then)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Condition Store Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_category_simple_discount(request, slug):
    form = AddSimpleDiscount_Category(request.POST or None)
    if form.is_valid():
        form = AddSimpleDiscount_Category()
    percent = request.POST.get("percent")
    category = request.POST.get("category")
    if percent is not None:
        answer = role_service.addSimpleDiscount_Category(user.getUserID(), int(slug), float(percent), category)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Category Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_category_simple_condition_discount(request, slug):
    form = AddSimpleConditionDiscount_Category(request.POST or None)
    if form.is_valid():
        form = AddSimpleConditionDiscount_Category()
    rule_type = request.POST.get("rule_type")
    percent = request.POST.get("percent")
    category = request.POST.get("category")
    less_then = request.POST.get("max_value")
    more_then = request.POST.get("min_value")
    if rule_type is not None:
        answer = role_service.addSimpleConditionDiscount_Category(user.getUserID(), int(slug), float(percent), rule_type,
                                                                  category, less_then, more_then)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Condition Category Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_product_simple_discount(request, slug):
    form = AddSimpleDiscount_Product(request.POST or None)
    if form.is_valid():
        form = AddSimpleDiscount_Product()
    percent = request.POST.get("percent")
    product_id = request.POST.get("product_ID")
    if percent is not None:
        answer = role_service.addSimpleDiscount_Category(user.getUserID(), int(slug), float(percent), product_id)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Product Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_product_simple_condition_discount(request, slug):
    form = AddSimpleConditionDiscount_Product(request.POST or None)
    if form.is_valid():
        form = AddSimpleConditionDiscount_Product()
    rule_type = request.POST.get("rule_type")
    percent = request.POST.get("percent")
    product_id = request.POST.get("product_ID")
    less_then = request.POST.get("max_value")
    more_then = request.POST.get("min_value")
    if rule_type is not None:
        answer = role_service.addSimpleConditionDiscount_Product(user.getUserID(), int(slug), float(percent), rule_type,
                                                                 product_id, less_then, more_then)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Simple Condition Product Discount",
        "form": form
    }
    return render(request, "form.html", context)


def add_condition_or(request, slug):
    form = AddConditionDiscountAndOr(request.POST or None)
    if form.is_valid():
        form = AddConditionDiscountAndOr()
    discount_ID = request.POST.get("discount_ID")
    rule_ID1 = request.POST.get("rule_ID1")
    rule_ID2 = request.POST.get("rule_ID2")
    if discount_ID is not None:
        answer = role_service.addConditionDiscountOr(user.getUserID(), int(slug), discount_ID, rule_ID1, rule_ID2)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Condition OR",
        "form": form
    }
    return render(request, "form.html", context)


def add_condition_xor(request, slug):
    form = AddConditionDiscountXor(request.POST or None)
    if form.is_valid():
        form = AddConditionDiscountXor()
    discount_ID = request.POST.get("discount_ID")
    rule_ID1 = request.POST.get("rule_ID1")
    rule_ID2 = request.POST.get("rule_ID2")
    decide = request.POST.get("decide")
    if discount_ID is not None:
        answer = role_service.addConditionDiscountXor(user.getUserID(), int(slug), int(discount_ID), int(rule_ID1),
                                                      int(rule_ID2), int(decide))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Condition XOR",
        "form": form
    }
    return render(request, "form.html", context)


def add_condition_and(request, slug):
    form = AddConditionDiscountAndOr(request.POST or None)
    if form.is_valid():
        form = AddConditionDiscountAndOr()
    discount_ID = request.POST.get("discount_ID")
    rule_ID1 = request.POST.get("rule_ID1")
    rule_ID2 = request.POST.get("rule_ID2")
    if discount_ID is not None:
        answer = role_service.addConditionDiscountAnd(user.getUserID(), int(slug), int(discount_ID), int(rule_ID1),
                                                      int(rule_ID2))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Add Condition AND",
        "form": form
    }
    return render(request, "form.html", context)


def remove_condition(request, slug):
    form = RemoveDiscount(request.POST or None)
    if form.is_valid():
        form = RemoveDiscount()
    discount_ID = request.POST.get("discount_ID")
    if discount_ID is not None:
        answer = role_service.removeDiscount(user.getUserID(), int(slug), int(discount_ID))
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Remove Discount",
        "form": form
    }
    return render(request, "form.html", context)

def remove_Owner(request, slug):
    global user
    form = RemoveForm(request.POST or None)
    if form.is_valid():
        form = RemoveForm()
    owner_name = request.POST.get("owner_name")
    if owner_name is not None:
        answer = role_service.removeStoreOwner(int(slug), user.getUserID(), owner_name)
        if not answer.isError():
            return HttpResponseRedirect("/store/" + slug + "/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Remove Store Owner",
        "form": form
    }
    return render(request, "form.html", context)


def remove_member(request):
    global user
    form = RemoveMemberForm(request.POST or None)
    if form.is_valid():
        form = RemoveMemberForm()
    member_name = request.POST.get("member_name")
    if member_name is not None:
        answer = role_service.removeMember(user.getMemberName(), member_name)
        if not answer.isError():
            return HttpResponseRedirect("/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Remove Member Owner",
        "form": form
    }
    return render(request, "form.html", context)


def all_stores_transactions(request):
    answer = role_service.getAllStoreTransactions(user.getMemberName())
    stores_transactions = []
    if not answer.isError():
        stores_transactions = answer.getData()
    context = {"title": "All Stores Transaction", "transactions": stores_transactions}
    return render(request, "transactions.html", context)


def all_user_transactions(request):
    answer = role_service.getAllUserTransactions(user.getMemberName())
    user_transactions = []
    if not answer.isError():
        user_transactions = answer.getData()
    context = {"title": "All Users Transaction", "transactions": user_transactions}
    return render(request, "transactions.html", context)


def store_transactions(request):
    global user
    form = StoreTransactions(request.POST or None)
    if form.is_valid():
        form = StoreTransactions()
    transactions_ID = request.POST.get("transactions_ID")
    if transactions_ID is not None:
        answer = role_service.getStoreTransaction(user.getMemberName(), int(transactions_ID))
        if not answer.isError():
            return HttpResponseRedirect("/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Stores Transactions",
        "form": form
    }
    return render(request, "form.html", context)

def user_transactions(request):
    global user
    form = UserTransactions(request.POST or None)
    if form.is_valid():
        form = UserTransactions()
    user_ID = request.POST.get("user_ID")
    if user_ID is not None:
        answer = role_service.getUserTransaction(user.getMemberName(), user_ID)
        if not answer.isError():
            return HttpResponseRedirect("/")
        messages.warning(request, answer.getError())
    context = {
        "title": "User Transactions",
        "form": form
    }
    return render(request, "form.html", context)

def store_transactions_ID(request):
    global user
    form = StoreTransactionsByID(request.POST or None)
    if form.is_valid():
        form = StoreTransactionsByID()
    store_ID = request.POST.get("store_ID")
    if store_ID is not None:
        answer = role_service.getStoreTransactionByStoreId(user.getMemberName(), int(store_ID))
        if not answer.isError():
            return HttpResponseRedirect("/")
        messages.warning(request, answer.getError())
    context = {
        "title": "Stores Transactions By StoreID",
        "form": form
    }
    return render(request, "form.html", context)
