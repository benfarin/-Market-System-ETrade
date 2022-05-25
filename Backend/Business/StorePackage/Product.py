from typing import List
import zope
from zope.interface import implements

from Backend.Exceptions.CustomExceptions import ProductException
from Backend.Interfaces.IProduct import IProduct


@zope.interface.implementer(IProduct)
class Product:

    def __init__(self, Id, storeId, name, price, category, weight, keyword):
        self.__id = Id
        self.__storeId = storeId
        self.__name = name
        self.__price = price
        self.__category = category  # String
        self.__weight = weight
        self.__keywords: List = keyword

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

    def getProductKeywords(self):
        return self.__keywords

    def setProductName(self, name):
        if name is None:
            raise ProductException("name of a product cannot be None")
        self.__name = name

    def setProductPrice(self, price):
        if price <= 0:
            raise ProductException("price of a product cannot be non-positive")
        self.__price = price

    def setProductCategory(self, category):
        if category is None:
            raise ProductException("category of a product cannot be None")
        self.__category = category

    def setProductWeight(self, weight):
        if weight <= 0:
            raise ProductException("weight of a product cannot be non-positive")
        self.__weight = weight

    def addKeyWord(self, keyword):
        if keyword not in self.__keywords:
            self.__keywords.append(keyword)

    def removeKeyWord(self, keyword):
        if keyword not in self.__keywords:
            raise Exception("cannot remove keyword that doesn't exists")
        self.__keywords.remove(keyword)

    def isExistsKeyword(self, keyword):
        for keyw in self.__keywords:
            if keyw.lower() == keyword.lower():
                return True
        return False

