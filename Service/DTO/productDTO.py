from typing import List
class productDTO:
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
