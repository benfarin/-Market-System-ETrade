from typing import Dict
import datetime
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from ModelsBackend.models import StoreTransactionModel


class StoreTransaction:

    def __init__(self, storeId, storeName, transactionId, paymentId, products, amount):
        # self.__storeId = storeId
        # self.__storeName = storeName
        # self.__transactionId = transactionId
        # self.__payemntId = paymentId
        # self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        # self.__products = products
        # self.__amount = amount
        self.__st = StoreTransactionModel(storeId=storeId, storeName=storeName, transactionId= transactionId,
                                          paymentId=paymentId, )
        self.__p = ProductModel(product_id=Id, storeId=storeId, name=name, price=price,
                                category=category
                                , weight=weight)
        self.__p.save()

    def getStoreId(self):
        return self.__storeId

    def getStoreName(self):
        return self.__storeName

    def getTransactionID(self):
        return self.__transactionId

    def getPaymentId(self):
        return self.__payemntId

    def getAmount(self):
        return self.__amount

    def getProducts(self):
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
