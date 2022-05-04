from typing import List

import zope
from zope.interface import implements

from interfaces.IProduct import IProduct


@zope.interface.implementer(IProduct)
class Product(implements(IProduct)):

    def __init__(self, Id, name, price, category, keyword):
        self.__id = Id
        self.__name = name
        self.__price = price
        self.__category = category  # String
        self.__keywords: List = keyword

    def getProductId(self):
        return self.__id

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def getProductCategory(self):
        return self.__category

    def setProductName(self, name):
        self.__name = name

    def setProductPrice(self, price):
        self.__price = price

    def setProductCategory(self, category):
        self.__category = category

    def addKeyWord(self, keyword):
        if keyword not in self.__keywords:
            self.__keywords.append(keyword)

    def removeKeyWord(self, keyword):
        if keyword not in self.__keywords:
            raise Exception("cannot remove keyword that doesn't exists")
        self.__keywords.remove(keyword)

    def isExistsKeyword(self, keyword):
        return keyword in self.__keywords

    def printForEvents(self):
        productStr = "\n\t\t\tid: " + str(self.__id)
        productStr += "\n\t\t\tname: " + self.__name
        productStr += "\n\t\t\tprice: " + str(self.__price)
        productStr += "\n\t\t\tcategory: " + self.__category
        productStr += "\n\t\t\tkeywords: "
        for keyword in self.__keywords:
            productStr += "\n\t\t\t\t" + keyword
        return productStr
