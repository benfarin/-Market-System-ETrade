import datetime
from Backend.Service.DTO import ProductDTO
from typing import Dict
from Backend.Business.Transactions.StoreTransaction import StoreTransaction


class storeTransactionForUserDTO:

    def __init__(self, StoreTransaction: StoreTransaction):
        self.__storeName = StoreTransaction.getStoreName()
        self.__products: Dict[ProductDTO: int] = {}
        for product in StoreTransaction.getProducts():
            self.__products[product.getProductId()] = product
        self.__amount = StoreTransaction.getAmount()

    def getProducts(self):
        return self.__products

    def getProduct(self, productID):
        self.__products.get(productID)

    def getAmount(self):
        return self.__amount

    def setName(self, name):
        self.__storeName = name

    def setProducts(self, products):
        self.__products = products

    def setAmount(self, amount):
        self.__amount = amount

    def __str__(self):
        toReturn = "\tstore transaction of store " + self.__storeName + ":"
        toReturn += "\n\t\t\tproducts: "
        for product in self.__products.values():
            toReturn += "\n\t\t\t\tproduct: " + product.getProductName() + ", quantity: " + str(self.__products.get(product))
        return toReturn + "\n\t\t\tamount: " + str(self.__amount)

