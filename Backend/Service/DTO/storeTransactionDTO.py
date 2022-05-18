import datetime
from Backend.Service.DTO import ProductDTO
from typing import Dict
from Backend.Business.Transactions.StoreTransaction import StoreTransaction


class storeTransactionDTO:

    def __init__(self, storeTransaction: StoreTransaction):
        self.__storeId = storeTransaction.getStoreId()
        self.__transactionId = storeTransaction.getTransactionID()
        self.__payemntId = storeTransaction.getPaymentId()
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products: Dict[int: ProductDTO] = storeTransaction.getProducts()
        self.__amount = storeTransaction.getAmount()

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

    def __str__(self):
        toReturn = "store transaction of store: " + str(self.__storeId) + ":"
        toReturn += "\n\ttransaction id: " + str(self.__transactionId)
        toReturn += "\n\tpayment id: " + str(self.__payemntId)
        toReturn += "\n\tdate: " + str(self.__date)
        toReturn += "\n\tproducts: "
        for product in self.__products.values():
            toReturn += "\n\t" + product.__str__()
        return toReturn + "\n\tamount: " + str(self.__amount)
