import datetime
from Service.DTO import ProductDTO
from typing import Dict


class storeTransactionForUserDTO:

    def __init__(self, storeName, products, amount):
        self.__storeName = storeName
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products: Dict[int: ProductDTO] = products
        self.__amount = amount

    def getProducts(self):
        return self.__products

    def getProduct(self, productID):
        self.__products.get(productID)

    def getDate(self):
        return self.__date

    def getAmount(self):
        return self.__amount

    def setName(self, name):
        self.__storeName = name

    def setProducts(self, products):
        self.__products = products

    def setDate(self, date):
        self.__date = date

    def setAmount(self, amount):
        self.__amount = amount
