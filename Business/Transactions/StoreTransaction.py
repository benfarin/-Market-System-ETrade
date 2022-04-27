from typing import Dict
import datetime


class StoreTransaction:

    def __init__(self, storeId, transactionId, paymentId, products, amount):
        self.__storeId = storeId
        self.__transactionId = transactionId
        self.__payemntId = paymentId
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products = products
        self.__amount = amount

    def getTransactionID(self):
        return self.__transactionId

    def getProduts(self):
        return self.__products

    def getPurchaseHistoryInformation(self):
        info = " transactionId: " + str(self.__transactionId)
        info += "\n\tpaymentId: " + self.__payemntId
        info += "\n\tdate: " + str(self.__date)
        info += "\n\tproducts: "
        for product in self.__products.keys():
            info += "\n\t\t\tname: " + product.getProductName() + ", price: " + str(
                product.getProductPrice()) + ", amount: " + str(self.__products[product])
        info += "\n\ttotal amount: " + str(self.__amount) + "\n"
        return info
