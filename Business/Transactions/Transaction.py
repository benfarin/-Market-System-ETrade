import datetime
from Business.StorePackage.Product import Product
from typing import Dict


class Transaction:

    def __init__(self, transactionId, userId, storeId, products, amount):
        self.__transactionId = transactionId
        self.__userId = userId
        self.__storeId = storeId
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__products: Dict[Product: int] = products
        self.__amount = amount

    def __str__(self):
        info = " transactionId: " + str(self.__transactionId)
        info += "\n\t" + "userId: " + str(self.__userId)
        info += "\n\t" + "date: " + str(self.__date)
        info += "\n\t" + "products: "
        for product in self.__products.keys():
            info += "\n\t\tname: " + product.getProductName() + ", price: " + str(product.getProductPrice()) + ", amount: " + str(self.__products[product])
        info += "\n\ttotal amount: " + str(self.__amount) + "\n"
        return info



