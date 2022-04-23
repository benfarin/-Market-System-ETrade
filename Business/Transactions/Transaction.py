import datetime
from Business.StorePackage.Product import Product
from typing import Dict


class Transaction:

    def __init__(self, transactionId, userId, products, amount):
        self.__transactionId = transactionId
        self.__userId = userId
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products: Dict[int: Dict[Product: int]] = products  # [storeId : [Product: quantity]]
        self.__amount = amount

    def getTransactionID(self):
        return self.__transactionId

    def setTransactionID(self,newTransID):
        self.__transactionId = newTransID

    def getDate(self):
        return self.__date

    def getProducts(self):
        return self.__products


    def __str__(self):
        info = " transactionId: " + str(self.__transactionId)
        info += "\n\t" + "userId: " + str(self.__userId)
        info += "\n\t" + "date: " + str(self.__date)
        info += "\n\t" + "products: "
        for storeId in self.__products.keys():
            info += "\n\t\tstoreId: " + str(storeId)
            for product in self.__products[storeId]:
                info += "\n\t\t\tname: " + product.getProductName() + ", price: " + str(product.getProductPrice()) + ", amount: " + str(self.__products[product])
        info += "\n\ttotal amount: " + str(self.__amount) + "\n"
        return info



