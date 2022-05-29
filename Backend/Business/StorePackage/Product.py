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

    def __init__(self, Id=None, storeId=None, name=None, price=None, category=None, weight=None, keyword=None, model=None):
        # self.__id = Id
        # self.__storeId = storeId
        # self.__name = name
        # self.__price = price
        # self.__category = category  # String
        # self.__weight = weight
        # self.__keywords: List = keyword
        if model is None:
            self.__model = ProductModel.objects.get_or_create(product_id=Id, storeId=storeId, name=name, price=price,
                                                              category=category
                                                              , weight=weight)[0]

            for k in keyword:
                ProductKeyword.objects.get_or_create(product_id=self.__model, keyword=k)

        else:
            self.__model = model

    def getProductId(self):
        return self.__model.product_id

    def getProductStoreId(self):
        return self.__model.storeId

    def getProductName(self):
        return self.__model.name

    def getProductPrice(self):
        return self.__model.price

    def getProductCategory(self):
        return self.__model.category

    def getProductWeight(self):
        return self.__model.weight

    def getModel(self):
        return self.__model

    def getProductKeywords(self):
        keywords = []
        keywords_models = ProductKeyword.objects.filter(product_id=self.__model)
        for k in keywords_models:
            keywords.append(k.keyword)
        return keywords

    def setProductName(self, name):
        if name is None:
            raise ProductException("name of a product cannot be None")
        self.__model.name = name
        self.__model.save()

    def setProductPrice(self, price):
        if price <= 0:
            raise ProductException("price of a product cannot be non-positive")
        self.__model.price = price
        self.__model.save()

    def setProductCategory(self, category):
        if category is None:
            raise ProductException("category of a product cannot be None")
        self.__model.category = category
        self.__model.save()

    def setProductWeight(self, weight):
        if weight <= 0:
            raise ProductException("weight of a product cannot be non-positive")
        self.__model.weight = weight
        self.__model.save()

    def addKeyWord(self, keyword):
        if not ProductKeyword.objects.filter(product_id=self.__model, keyword=keyword).exists():
            k = ProductKeyword.objects.get_or_create(product_id=self.__model, keyword=keyword)[0]
            k.save()

    def removeKeyWord(self, keyword):
        if not ProductKeyword.objects.filter(product_id=self.__model, keyword=keyword).exists():
            raise Exception("cannot remove keyword that doesn't exists")
        ProductKeyword.objects.get(product_id=self.__model, keyword=keyword).delete()

    def isExistsKeyword(self, keyword):
        return ProductKeyword.objects.filter(product_id=self.__model, keyword=keyword).exists()

    def removeProduct(self):
        self.__model.delete()
