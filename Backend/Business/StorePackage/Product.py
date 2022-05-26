from typing import List
import zope
from zope.interface import implements
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Exceptions.CustomExceptions import ProductException
from Backend.Interfaces.IProduct import IProduct
from ModelsBackend.models import ProductModel, ProductKeyword


@zope.interface.implementer(IProduct)
class Product:

    def __init__(self, Id, storeId, name, price, category, weight, keyword):
        # self.__id = Id
        # self.__storeId = storeId
        # self.__name = name
        # self.__price = price
        # self.__category = category  # String
        # self.__weight = weight
        # self.__keywords: List = keyword
        self.__p = ProductModel(product_id=Id, storeId=storeId, name=name, price=price,
                                category=category
                                ,weight=weight)
        self.__p.save()

        for k in keyword:
            ProductKeyword.objects.get_or_create(product_id=self.__p, keyword=k)

    def getProductId(self):
        return self.__p.product_id

    def getProductStoreId(self):
        return self.__p.storeId

    def getProductName(self):
        return self.__p.name

    def getProductPrice(self):
        return self.__p.price

    def getProductCategory(self):
        return self.__p.category

    def getProductWeight(self):
        return self.__p.weight

    def getModel(self):
        return self.__p

    def getProductKeywords(self):
        keywords = []
        keywords_models = ProductKeyword.objects.filter(product_id=self.__p)
        for k in keywords_models:
            keywords.append(k.keyword)
        return keywords

    def setProductName(self, name):
        if name is None:
            raise ProductException("name of a product cannot be None")
        self.__p.name = name
        self.__p.save()

    def setProductPrice(self, price):
        if price <= 0:
            raise ProductException("price of a product cannot be non-positive")
        self.__p.price = price
        self.__p.save()

    def setProductCategory(self, category):
        if category is None:
            raise ProductException("category of a product cannot be None")
        self.__p.category = category
        self.__p.save()

    def setProductWeight(self, weight):
        if weight <= 0:
            raise ProductException("weight of a product cannot be non-positive")
        self.__p.weight = weight
        self.__p.save()

    def addKeyWord(self, keyword):
        if keyword not in self.__keywords:
            ProductKeyword.objects.get_or_create(product_id=self.__p, keyword=keyword)

    def removeKeyWord(self, keyword):
        if keyword not in self.__keywords:
            raise Exception("cannot remove keyword that doesn't exists")
        ProductKeyword.objects.get(product_id=self.__p, keyword=keyword).delete()

    def isExistsKeyword(self, keyword):
        return ProductKeyword.objects.get(product_id=self.__p, keyword=keyword) is not None

