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
    my_stores_page, create_store_page, store_page,
)

urlpatterns = [
    path('', home_page),
    path('my_stores/', my_stores_page),
    path('store/<str:slug>/', store_page),
    path('addstore/', create_store_page),
    path('signup/', signup_page),
    path('login/', login_page),
    path('admin/', admin.site.urls),
]
