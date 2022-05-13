"""mysite URL Configuration

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
from django.contrib import admin
from django.urls import path

from .views import (
    home_page,
    signup_page,
    login_page,
    my_stores_page, create_store_page, store_page, store_products_management, appoint_manager, appoint_Owner, logout,
    add_product, get_cart, add_to_cart_page, purchase_cart, search_view, show_history, product_update, remove_product,
    add_quantity, purchases_page, permissions_page,
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
    path('store/<str:slug>/appoint_manager/', appoint_manager),
    path('store/<str:slug>/appoint_owner/', appoint_Owner),
    path('store/<str:slug>/stuff_permissions/', permissions_page),
    # path('store/<str:slug>/stuff/', show_stuff),
    path('store/<str:slug>/history/', show_history),
    path('addstore/', create_store_page),
    path('signup/', signup_page),
    path('login/', login_page),
    path('logout/', logout),
    path('cart/', get_cart),
    path('cart/purchase_cart/', purchase_cart),
    path('store/<str:slug>/add_to_cart/<str:slug2>/', add_to_cart_page),
    path('search/', search_view),
    path('purchases/', purchases_page),
    path('admin/', admin.site.urls),
]
