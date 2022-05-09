from typing import List

from Business.StorePackage.Product import Product


class ProductDTO:
    def __init__(self, product: Product):
        self.__productId = product.getProductId()
        self.__name = product.getProductName()
        self.__price = product.getProductPrice()
        self.__category = product.getProductCategory() # String
        self.__keywords: List = product.getProductKeywords()

    def getProductId(self):
        return self.__productId

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def getProductCategory(self):
        return self.__category

    def getKeyWords(self):
        return self.__keywords

    def setProductName(self, name):
        self.__name = name

    def setProductID(self,productID):
        self.__id = productID

    def setProductPrice(self, price):
        self.__price = price

    def setCatagory(self, catagory):
        self.__category = catagory

    def setKeyWords(self, keywords):
        self.__keywords = keywords
