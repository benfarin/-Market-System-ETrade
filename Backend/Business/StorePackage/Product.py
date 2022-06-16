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

            self.__id = Id
            self.__storeId = storeId
            self.__name = name
            self.__price = price
            self.__category = category
            self.__weight = weight
            for k in keyword:
                lowerKeyword = k.lower()
                ProductKeyword.objects.get_or_create(product_id=self.__model, keyword=lowerKeyword)

        else:
            self.__model = model
            self.__id = self.__model.product_id
            self.__storeId = self.__model.storeId
            self.__name = self.__model.name
            self.__price = self.__model.price
            self.__category = self.__model.category
            self.__weight = self.__model.weight

    def getProductId(self):
        return self.__id

    def getProductStoreId(self):
        return self.__storeId

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def getProductCategory(self):
        return self.__category

    def getProductWeight(self):
        return self.__weight

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
        self.__name = name

    def setProductPrice(self, price):
        if price <= 0:
            raise ProductException("price of a product cannot be non-positive")
        self.__model.price = price
        self.__model.save()
        self.__price = price

    def setProductCategory(self, category):
        if category is None:
            raise ProductException("category of a product cannot be None")
        self.__model.category = category
        self.__model.save()
        self.__category = category

    def setProductWeight(self, weight):
        if weight <= 0:
            raise ProductException("weight of a product cannot be non-positive")
        self.__model.weight = weight
        self.__model.save()
        self.__weight = weight

    def addKeyWord(self, keyword):
        if not ProductKeyword.objects.filter(product_id=self.__model, keyword=keyword).exists():
            k = ProductKeyword.objects.get_or_create(product_id=self.__model, keyword=keyword)[0]
            k.save()

    def removeKeyWord(self, keyword):
        if not ProductKeyword.objects.filter(product_id=self.__model, keyword=keyword).exists():
            raise Exception("cannot remove keyword that doesn't exists")
        ProductKeyword.objects.get(product_id=self.__model, keyword=keyword).delete()

    def isExistsKeyword(self, keyword):
        lowerKeyword = keyword.lower()
        return ProductKeyword.objects.filter(product_id=self.__model, keyword=lowerKeyword).exists()

    def removeProduct(self):
        if self.__model.product_id is not None:
            for pk in ProductKeyword.objects.filter(product_id=self.__model):
                pk.delete()
            self.__model.delete()

    def __eq__(self, other):
        return isinstance(other, Product) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.product_id)
