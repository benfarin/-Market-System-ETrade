"""Frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include

from .views import (
    home_page,
    signup_page,
    login_page,
    my_stores_page, create_store_page, store_page, store_products_management, appoint_manager, appoint_Owner,
    add_product, get_cart, add_to_cart_page, purchase_cart, search_view, show_history, product_update, remove_product,
    add_quantity, purchases_page, permissions_page, remove_product_from_cart, close_store, discounts_page,
    add_condition_add, add_condition_max, add_rule, add_store_simple_discount,
    add_store_simple_condition_discount, add_category_simple_discount, add_category_simple_condition_discount,
    add_product_simple_discount, add_product_simple_condition_discount, remove_condition, remove_Owner, remove_member,
    all_stores_transactions, all_user_transactions, store_transactions, user_transactions, store_transactions_ID,
    show_store_transactions_ID, show_user_transactions, show_store_transactions, remove_product_from_cart_with_store,
    add_condition_or, add_condition_xor, add_condition_and, logout_page, add_purchase_rule, getStoreBids, bid_page,
    accept_bid,
)

urlpatterns = [
    path('', home_page),
    path('my_stores/', my_stores_page),
    path('store/<str:slug>/', store_page),
    path('store/<str:slug>/<str:slug2>/products_manage/', store_products_management),
    path('store/<str:slug>/<str:slug2>/products_manage/product_update/', product_update),
    path('store/<str:slug>/<str:slug2>/products_manage/remove_product/', remove_product),
    path('store/<str:slug>/<str:slug2>/products_manage/quantity/', add_quantity),
    path('store/<str:slug>/addproduct/', add_product),
    path('store/<str:slug>/close/', close_store),
    path('store/<str:slug>/appoint_manager/', appoint_manager),
    path('store/<str:slug>/appoint_owner/', appoint_Owner),
    path('store/<str:slug>/remove_owner/', remove_Owner),
    path('store/<str:slug>/stuff_permissions/', permissions_page),
    path('store/<str:slug>/discounts/', discounts_page),
    path('remove_member/', remove_member),
    path('all_stores_transactions/', all_stores_transactions),
    path('all_users_transactions/', all_user_transactions),
    path('store_transactions/', store_transactions),
    path('user_transactions/', user_transactions),
    path('store_transactions_ID/', store_transactions_ID),
    path('<str:slug>/storesTransactions/', show_store_transactions),
    path('<str:slug>/userTransactions/', show_user_transactions),
    path('<str:slug>/storesTransactionsID/', show_store_transactions_ID),
    path('store/<str:slug>/discounts/add_store_simple_discount/', add_store_simple_discount),
    path('store/<str:slug>/discounts/add_store_simple_condition_discount/', add_store_simple_condition_discount),
    path('store/<str:slug>/discounts/add_category_simple_discount/', add_category_simple_discount),
    path('store/<str:slug>/discounts/add_category_simple_condition_discount/', add_category_simple_condition_discount),
    path('store/<str:slug>/discounts/add_product_simple_discount/', add_product_simple_discount),
    path('store/<str:slug>/discounts/add_product_simple_condition_discount/', add_product_simple_condition_discount),
    path('store/<str:slug>/discounts/add_condition_max/', add_condition_max),
    path('store/<str:slug>/discounts/add_condition_add/', add_condition_add),
    path('store/<str:slug>/discounts/add_condition_or/', add_condition_or),
    path('store/<str:slug>/discounts/add_condition_xor/', add_condition_xor),
    path('store/<str:slug>/discounts/add_condition_and/', add_condition_and),
    path('store/<str:slug>/discounts/remove_discount/', remove_condition),
    path('store/<str:slug>/discounts/add_rule/', add_rule),
    path('store/<str:slug>/purchase_rules/', add_purchase_rule),
    path('store/<str:slug>/bids/', getStoreBids),
    path('store/<str:slug>/bids/<str:slug2>/', bid_page),
    path('store/<str:slug>/bids/<str:slug2>/accept/', accept_bid),
    path('store/<str:slug>/bids/<str:slug2>/reject/', bid_page),
    path('store/<str:slug>/bids/<str:slug2>/offeralternate/', bid_page),
    # path('store/<str:slug>/stuff/', show_stuff),
    path('store/<str:slug>/history/', show_history),
    path('addstore/', create_store_page),
    path('signup/', signup_page),
    path('login/', login_page),
    path('logout/', logout_page),
    path('cart/', get_cart),
    path('cart/<str:slug>/remove_product/', remove_product_from_cart),
    path('cart/<str:slug>/<str:slug2>/remove_product/', remove_product_from_cart_with_store),
    path('cart/purchase_cart/', purchase_cart),
    path('store/<str:slug>/add_to_cart/<str:slug2>/', add_to_cart_page),
    path('search/', search_view),
    path('search/add_to_cart/<str:slug>/<str:slug2>/', add_to_cart_page),
    path('purchases/', purchases_page),
    path('admin/', admin.site.urls),
]
