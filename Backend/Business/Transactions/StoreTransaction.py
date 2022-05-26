from typing import Dict
import datetime
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from ModelsBackend.models import StoreTransactionModel, ProductsInStoreTransactions


class StoreTransaction:

    def __init__(self, storeId, storeName, transactionId, paymentId, products, amount):
        # self.__storeId = storeId
        # self.__storeName = storeName
        # self.__transactionId = transactionId
        # self.__payemntId = paymentId
        # self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        # self.__products = products
        # self.__amount = amount
        self.__st = StoreTransactionModel(storeId=storeId, storeName=storeName, transactionId=transactionId,
                                          paymentId=paymentId, date=datetime.datetime.now(), amount=amount)
        self.__st.save()
        for product in products:
            ProductsInStoreTransactions(transactionId=self.__st, productId=product).save()

    def getStoreId(self):
        return self.__st.storeId

    def getStoreName(self):
        return self.__st.storeName

    def getTransactionID(self):
        return self.__st.transactionId

    def getPaymentId(self):
        return self.__st.paymentId

    def getAmount(self):
        return self.__st.amount

    def getProducts(self):
        return [pm.productId for pm in ProductsInStoreTransactions.objects.filter(transactionId=self.__st.transactionId)]

    def getModel(self):
        return self.__st

    # can be deleted in this version
    def getPurchaseHistoryInformation(self):
        pass
        # info = " transactionId: " + str(self.__transactionId)
        # info += "\n\tpaymentId: " + self.__payemntId
        # info += "\n\tdate: " + str(self.__date)
        # info += "\n\tproducts: "
        # for product in self.__products.keys():
        #     info += "\n\t\t\tname: " + product.getProductName() + ", price: " + str(
        #         product.getProductPrice()) + ", amount: " + str(self.__products[product])
        # info += "\n\ttotal amount: " + str(self.__amount) + "\n"
        # return info
