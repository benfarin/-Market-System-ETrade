from typing import List

from Backend.Business.StorePackage.Product import Product


class ProductDTO:
    def __init__(self, product: Product):
        self.__productId = product.getProductId()
        self.__storeId = product.getProductStoreId()
        self.__name = product.getProductName()
        self.__price = product.getProductPrice()
        self.__category = product.getProductCategory()  # String
        self.__wight = product.getProductWeight()
        self.__keywords: List = product.getProductKeywords()

    def getProductId(self):
        return self.__productId

    def getProductStoreId(self):
        return self.__storeId

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def getProductCategory(self):
        return self.__category

    def getProductWeight(self):
        return self.__wight

    def getKeyWords(self):
        return self.__keywords

    def setProductName(self, name):
        self.__name = name

    def setProductID(self, productID):
        self.__id = productID

    def setProductPrice(self, price):
        self.__price = price

    def setCatagory(self, catagory):
        self.__category = catagory

    def setProductWeight(self, weight):
        self.__wight = weight

    def setKeyWords(self, keywords):
        self.__keywords = keywords

    def __str__(self):
        toReturn = "product: " + str(self.__productId) + ":"
        toReturn += "\n\tname: " + self.__name
        toReturn += "\n\tprice: " + str(self.__price)
        toReturn += "\n\tcategory: " + str(self.__category)
        toReturn += "\n\tweight: " + str(self.__wight)
        toReturn += "\n\tkeywords: "
        for keyword in self.__keywords:
            toReturn += "\n\t\t" + keyword
        return toReturn

    def printInBag(self):
        toReturn = "product: " + str(self.__productId) + ":"
        toReturn += "\n\t\t\t\t\t\tstoreId: " + str(self.__storeId)
        toReturn += "\n\t\t\t\t\t\tname: " + self.__name
        toReturn += "\n\t\t\t\t\t\tprice: " + str(self.__price)
        toReturn += "\n\t\t\t\t\t\tcategory: " + str(self.__category)
        toReturn += "\n\t\t\t\t\t\tweight: " + str(self.__wight)
        toReturn += "\n\t\t\t\t\t\tkeywords: "
        for keyword in self.__keywords:
            toReturn += "\n\t\t\t\t\t\t\t" + keyword
        return toReturn
