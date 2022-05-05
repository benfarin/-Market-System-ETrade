import datetime
from Service.DTO import ProductDTO
from typing import Dict


class storeTransactionDTO:

    def __init__(self, storeId, transactionId, paymentId, products, amount):
        self.__storeId = storeId
        self.__transactionId = transactionId
        self.__payemntId = paymentId
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products: Dict[int: ProductDTO] = products
        self.__amount = amount

    def getTransactionID(self):
        return self.__transactionId

    def getProduts(self):
        return self.__products

    def getproduct(self, productID):
        self.__products.get(productID)

    def getStoreID(self):
        return self.__storeId

    def getPaymentID(self):
        return self.__payemntId

    def getDate(self):
        return self.__date

    def getAmount(self):
        return self.__amount

    def setTransactionID(self, id):
        self.__transactionId = id

    def setProduts(self, products):
        self.__products = products

    def setStoreID(self, storeid):
        self.__storeId = storeid

    def setPaymentID(self, payment):
        self.__payemntId = payment

    def setDate(self, date):
        self.__date = date

    def setAmount(self, amount):
        self.__amount = amount
